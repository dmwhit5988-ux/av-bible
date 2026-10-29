"""The Azure path, offline: IPA conversion, the SSML a verse becomes, which
engine speaks it, the usage meter, how use_ipa is saved, and when edge-tts
is asked again. Nothing here calls Azure or edge-tts.

    .venv\\Scripts\\python.exe -m unittest test_azure_tts -v
"""

import json
import os
import shutil
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest import mock

import azure_tts
import config
import pronunciation
import tts_engine


def phones(syllable):
    """A syllable of azure_ipa output split into its phones."""
    body, out, i = syllable.lstrip("ˈˌ"), [], 0
    every = pronunciation.AZURE_VOWELS | pronunciation.AZURE_CONSONANTS
    while i < len(body):
        if body[i:i + 2] in every:
            out.append(body[i:i + 2])
            i += 2
        elif body[i] in every:
            out.append(body[i])
            i += 1
        else:
            raise AssertionError(f"{body[i]!r} is not an Azure en-US phone")
    return out


class AzureIpa(unittest.TestCase):
    def check(self, ipa, want, possessive=False):
        self.assertEqual(pronunciation.azure_ipa(ipa, possessive), want, ipa)

    def test_stress_moves_to_the_start_of_a_dotted_syllable(self):
        # Undotted, Azure would stress the syllable before the mark.
        self.check("/mɪˈθuː.ʃeɪ.ɛl/", "mɪ.ˈθu.ʃeɪ.ɛl")
        self.check("/juːˈfreɪ.tiːz/", "ju.ˈfɹeɪ.tiz")
        self.check("/kælˈdiːz/", "kæl.ˈdiz")

    def test_espeak_style_marks_before_the_vowel(self):
        self.check("/mˈɔrdəkaɪ/", "ˈmɔɹ.də.kaɪ")
        self.check("/tˈaɪdəl/", "ˈtaɪ.dəl")
        self.check("/ʃˈɚ/", "ˈʃɝ")                    # stressed er is ɝ

    def test_diphthongs_win_over_centring_vowels(self):
        # The ɪə inside aɪə is not the British NEAR vowel.
        self.check("/ˌd͡ʒɛdɪˈdaɪə/", "ˌdʒɛ.dɪ.ˈdaɪ.ə")
        self.check("/ˈdʒeɪəl/", "ˈdʒeɪ.əl")

    def test_british_vowels_take_american_values(self):
        self.check("/ˈdʒɛər.ɛd/", "ˈdʒɛɹ.ɛd")
        self.check("/ɪər/", "ɪɹ")
        self.check("/jʊəˈɹaɪə/", "jʊ.ˈɹaɪ.ə")
        self.check("/ɜːr/", "ɝ")
        self.check("/ˈɡɜːr.ʃɒn/", "ˈgɝ.ʃɑn")
        self.check("/ˈzəʊ.ɑː/", "ˈzoʊ.ɑ")
        self.check("/ˈɡoʊ.mər/", "ˈgoʊ.mɚ")

    def test_yod_drops_in_an_onset_only(self):
        self.check("/kəˈtjʊər.ə/", "kə.ˈtʊɹ.ə")      # not "kuh-CHOOR-uh"
        self.check("/ˈzjuː.ɑːr/", "ˈzu.ɑɹ")
        self.check("/ˈmæθ.juː/", "ˈmæθ.ju")          # across a break it stays
        self.check("/ˈnɛm.jʊ.əl/", "ˈnɛm.jʊ.əl")
        self.check("/ˈhjuː.ɡoʊ/", "ˈhju.goʊ")         # h isn't dropped before
        self.check("/ˈseɪljʊ/", "ˈseɪl.jʊ")           # unstressed: kept, as in "value"
        self.check("/zjʊ.ri.ˈʃæd.aɪ/", "zʊ.ɹi.ˈʃæd.aɪ")  # first syllable: dropped

    def test_marks_azure_rejects_are_rewritten(self):
        self.check("/ˈtɑː(r)tərəs/", "ˈtɑɹ.tə.ɹəs")        # parentheses: HTTP 400
        self.check("/əˈbæ.dn̩/", "ə.ˈbæ.dən")              # syllabic n
        self.check("/ˌoʊ.bɛd ˈiː.dəm/", "ˌoʊ.bɛd.ˈi.dəm")  # space between words
        self.check("/ˈzam.zʌmˌmɪm/", "ˈzæm.zʌm.ˌmɪm")       # bare a

    def test_possessive(self):
        self.check("/ˈmoʊ.zɪz/", "ˈmoʊ.zɪz.ɪz", possessive=True)
        self.check("/ˈdʒeɪ.kəb/", "ˈdʒeɪ.kəbz", possessive=True)
        self.check("/sɛθ/", "sɛθs", possessive=True)

    def test_centring_vowels_are_diphthongs_only_before_r_or_at_the_end(self):
        self.check("/ˈsæmjʊəl/", "ˈsæ.mjʊ.əl")        # "SAM-yoo-el", not "SAM-yurl"
        self.check("/ˈɡɪdɪən/", "ˈgɪ.dɪ.ən")
        self.check("/nɪə/", "nɪɹ")                    # "near"
        self.check("/bɪəd/", "bɪɹd")                  # the only vowel: "beard"
        self.check("/ˈkʊəl.ɪŋ/", "ˈkʊɹl.ɪŋ")          # stressed: one syllable
        self.check("/ˈbɛər.ə/", "ˈbɛɹ.ə")

    def test_british_e_and_espeak_long_vowels(self):
        self.check("/ˈbeθəl/", "ˈbɛ.θəl")             # British e is the vowel of "bed"
        self.check("/seːp/", "seɪp")                  # the Verifier's eː is "say"
        self.check("/ɡoː/", "goʊ")

    def test_verifier_notation_and_alternatives(self):
        self.check("/mɛθuːsᵻlə/", "mɛ.θu.sɪ.lə")      # eSpeak's ᵻ, as "Use heard IPA" writes
        self.check("/ˈbɛç/", "ˈbɛh")                  # ç survives NFD
        self.check("/hævilɑ / hævɪlɐ/", "hæ.vi.lɑ")    # two readings: the first
        self.check("/ˈæ.rən/, /ˈɛr.ən/", "ˈæ.ɹən")

    def test_unsendable(self):
        for ipa in ("", "/ˈ./", "/ʘa/"):
            with self.subTest(ipa=ipa), self.assertRaises(ValueError):
                pronunciation.azure_ipa(ipa)

    def test_every_stored_ipa_converts_cleanly(self):
        names = pronunciation.load(force=True)
        failures = []
        for name, info in names.items():
            ipa = info.get("ipa")
            if not ipa:
                continue
            try:
                out = pronunciation.azure_ipa(ipa)
                for syl in out.split("."):
                    vowels = [p for p in phones(syl)
                              if p in pronunciation.AZURE_VOWELS]
                    if len(vowels) != 1 or "ˈ" in syl[1:] or "ˌ" in syl[1:]:
                        raise ValueError(f"bad syllable {syl!r} in {out}")
            except (ValueError, AssertionError) as e:
                failures.append(f"{name} {ipa}: {e}")
        self.assertEqual(failures, [], "\n".join(failures[:20]))


class IpaKeyboard(unittest.TestCase):
    """The Pronunciation Studio's keyboard offers Azure's phones, no more."""

    def test_keys_are_exactly_azures_phone_set(self):
        import ipa_keyboard
        self.assertEqual(ipa_keyboard.symbols(),
                         pronunciation.AZURE_VOWELS | pronunciation.AZURE_CONSONANTS)

    def test_every_key_types_ipa_azure_takes(self):
        import ipa_keyboard
        for sym in ipa_keyboard.symbols():
            with self.subTest(sym=sym):
                ipa = sym if sym in pronunciation.AZURE_VOWELS else "ˈæ." + sym + "ə"
                pronunciation.azure_ipa(ipa)


class Ssml(unittest.TestCase):
    """ssml(), uses_ipa() and respell() over a small list of our own."""

    NAMES = {
        "Methuselah": {"say": "muh-THOO-zuh-luh", "ipa": "/mɪˈθjuː.zə.lə/",
                       "ref": "Genesis 5:21", "override": True, "use_ipa": True},
        "Havilah": {"say": "HAV-ih-lah", "ipa": "/ˈhæv.ɪ.lə/",
                    "ref": "Genesis 2:11", "override": True},
        "Ham": {"say": "hamm", "ref": "Genesis 5:32", "override": True},
        "Enoch": {"say": "Enoch", "ipa": "/ˈiː.nək/", "ref": "Genesis 4:17",
                  "override": False},
        "Broken": {"say": "Broken", "ipa": "/ʘ/", "ref": "Genesis 1:1",
                   "override": False, "use_ipa": True},
    }

    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"names": self.NAMES}, f, ensure_ascii=False)
        # Cleanups run last-first: unpatch, then reload the real list.
        self.addCleanup(lambda: pronunciation.load(force=True))
        patcher = mock.patch.object(pronunciation, "JSON_PATH", self.path)
        patcher.start()
        self.addCleanup(patcher.stop)
        pronunciation.load(force=True)

    def tearDown(self):
        os.remove(self.path)

    def test_ipa_names_become_phonemes_and_the_rest_respell(self):
        body = pronunciation.ssml("Methuselah's son & Havilah <Hamath> Ham.")
        self.assertEqual(
            body,
            '<phoneme alphabet="ipa" ph="mɪ.ˈθu.zə.ləz">Methuselah\'s</phoneme>'
            " son &amp; hav-ih-lah &lt;Hamath&gt; hamm.")

    def test_left_curly_possessive_goes_inside_too(self):
        # WEB writes "Yahweh‘s" (U+2018) twice; a stranded ‘s is read "ess".
        self.assertIn("Methuselah‘s</phoneme> son",
                      pronunciation.ssml("Methuselah‘s son"))

    def test_edge_still_respells(self):
        self.assertEqual(pronunciation.respell("Methuselah and Enoch"),
                         "muh-thoo-zuh-luh and Enoch")

    def test_uses_ipa(self):
        self.assertTrue(pronunciation.uses_ipa("the days of Methuselah"))
        self.assertFalse(pronunciation.uses_ipa("Havilah and Enoch"))

    def test_unsendable_ipa_falls_back_and_is_reported(self):
        self.assertFalse(pronunciation.uses_ipa("Broken"))
        self.assertEqual(pronunciation.ssml("Broken"), "Broken")
        self.assertIn("no Azure en-US equivalent", pronunciation.ipa_problem("Broken"))
        self.assertEqual(pronunciation.ipa_problem("Methuselah"), "")

    def test_route_by_engine(self):
        voice, rate = tts_engine.HOUSE_VOICE, 0
        ipa_text, plain = "Methuselah lived.", "Havilah lived."
        edge = tts_engine.route(ipa_text, voice, rate, tts_engine.ENGINE_EDGE)
        self.assertEqual((edge.engine, edge.chars), (tts_engine.ENGINE_EDGE, 0))
        self.assertEqual(edge.payload, "muh-thoo-zuh-luh lived.")

        mixed = tts_engine.route(ipa_text, voice, rate, tts_engine.ENGINE_MIXED)
        self.assertEqual(mixed.engine, tts_engine.ENGINE_AZURE)
        self.assertIn("<phoneme", mixed.payload)
        self.assertIn("_ssml_", os.path.basename(mixed.path))
        self.assertEqual(mixed.chars, len(mixed.payload))

        self.assertEqual(
            tts_engine.route(plain, voice, rate, tts_engine.ENGINE_MIXED).engine,
            tts_engine.ENGINE_EDGE)

        # Plain text on Azure shares Edge's cache entry: the audio is the same.
        az = tts_engine.route(plain, voice, rate, tts_engine.ENGINE_AZURE)
        self.assertEqual(az.engine, tts_engine.ENGINE_AZURE)
        self.assertEqual(az.path, tts_engine.route(plain, voice, rate).path)

    def test_ipa_only_for_en_us_voices(self):
        # azure_ipa writes en-US phones; a British voice respells instead.
        r = tts_engine.route("Methuselah lived.", "en-GB-RyanNeural", 0,
                             tts_engine.ENGINE_MIXED)
        self.assertEqual(r.engine, tts_engine.ENGINE_EDGE)
        self.assertEqual(r.payload, "muh-thoo-zuh-luh lived.")

    def test_ipa_in_use(self):
        self.assertTrue(pronunciation.ipa_in_use(self.NAMES["Methuselah"]))
        self.assertFalse(pronunciation.ipa_in_use(self.NAMES["Broken"]))
        self.assertFalse(pronunciation.ipa_in_use(self.NAMES["Enoch"]))

    def test_rate_is_markup_only_when_not_zero(self):
        r = tts_engine.route("Methuselah.", tts_engine.HOUSE_VOICE, 10,
                             tts_engine.ENGINE_MIXED)
        self.assertTrue(r.payload.startswith('<prosody rate="+10%">'))


class VerseWords(Ssml):
    """for_verse() and save_verse(): words one verse alone says differently."""

    VERSES = {"Acts 13:2": {"Separate Barnabas": "Sep-uh-rate Barnabas"}}

    def setUp(self):
        super().setUp()
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"names": {**self.NAMES, "Barnabas": {
                "say": "BAR-nuh-bus", "ref": "Acts 4:36", "override": True}},
                "verses": self.VERSES}, f, ensure_ascii=False)
        md = mock.patch.object(pronunciation, "MD_PATH", self.path + ".md")
        md.start()
        self.addCleanup(md.stop)
        self.addCleanup(lambda: os.path.exists(self.path + ".md")
                        and os.remove(self.path + ".md"))
        pronunciation.load(force=True)

    def test_only_that_verse_changes(self):
        text = "the Holy Spirit said, “Separate Barnabas and Saul for me"
        self.assertEqual(pronunciation.for_verse("Acts 13:2", text),
                         "the Holy Spirit said, “Sep-uh-rate Barnabas and Saul for me")
        self.assertEqual(pronunciation.for_verse("Acts 13:3", text), text)
        self.assertEqual(pronunciation.for_verse("", text), text)

    def test_route_applies_the_verse_then_the_names(self):
        text = "“Separate Barnabas and Saul.”"
        r = tts_engine.route(text, tts_engine.HOUSE_VOICE, 0, ref="Acts 13:2")
        self.assertEqual(r.payload, "“Sep-uh-rate bar-nuh-bus and Saul.”")
        plain = tts_engine.route(text, tts_engine.HOUSE_VOICE, 0)
        self.assertEqual(plain.payload, "“Separate bar-nuh-bus and Saul.”")
        verbatim = tts_engine.route(text, tts_engine.HOUSE_VOICE, 0,
                                    apply_respell=False, ref="Acts 13:2")
        self.assertEqual(verbatim.payload, text)

    def test_whole_word_and_case_sensitive(self):
        words = {"Separate": "Sep-uh-rate"}
        self.assertEqual(pronunciation.apply_words("separate Separated", words),
                         "separate Separated")

    def test_save_verse_keeps_names_and_other_verses(self):
        pronunciation.save_verse("Genesis 1:4", {"divided": "di-vided", " ": "x"})
        self.assertEqual(pronunciation.verse_words("Genesis 1:4"),
                         {"divided": "di-vided"})
        self.assertEqual(pronunciation.verse_words("Acts 13:2"),
                         self.VERSES["Acts 13:2"])
        self.assertIn("Barnabas", pronunciation.load())
        with open(self.path, encoding="utf-8") as f:
            self.assertEqual(list(json.load(f)["verses"]),
                             ["Genesis 1:4", "Acts 13:2"])     # canonical order
        pronunciation.save_verse("Genesis 1:4", {})
        self.assertEqual(pronunciation.verse_words("Genesis 1:4"), {})

    def test_saving_names_keeps_the_verses(self):
        names = pronunciation.load()
        base = json.loads(json.dumps(names))
        names["Ham"] = {**names["Ham"], "say": "hahm"}
        pronunciation.save_names(names, base=base)
        self.assertEqual(pronunciation.all_verse_words(), self.VERSES)

    def test_a_changed_verse_is_no_longer_current(self):
        import generate_showcase_audio as showcase_audio
        cache = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, cache, True)
        patcher = mock.patch.object(tts_engine, "AUDIO_CACHE_DIR", cache)
        patcher.start()
        self.addCleanup(patcher.stop)
        text, ref = "“Separate Barnabas and Saul.”", "Acts 13:2"
        voice, rate = tts_engine.HOUSE_VOICE, 0
        rendered = tts_engine.route(text, voice, rate, ref=ref).path
        with open(rendered, "wb") as f:
            f.write(b"x" * 600)
        published = os.path.join(cache, "Acts_13_2.mp3")
        with open(published, "wb") as f:
            f.write(b"x" * 600)                     # Audio copies the cache entry
        self.assertTrue(showcase_audio.is_current(text, ref, published, voice, rate))
        pronunciation.save_verse(ref, {"Separate": "Separayte"})
        self.assertFalse(showcase_audio.is_current(text, ref, published, voice, rate))


class Meter(unittest.TestCase):
    def test_usage_sums_the_last_30_days_and_skips_junk(self):
        now = datetime.now(timezone.utc)
        lines = [
            {"t": (now - timedelta(days=40)).isoformat(), "chars": 1000},
            {"t": (now - timedelta(days=2)).isoformat(), "chars": 250},
            {"t": now.isoformat(), "chars": 50, "what": "Genesis 1:1"},
        ]
        fd, path = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(json.dumps(line) + "\n")
            f.write("not json\n")
        try:
            with mock.patch.object(config, "AZURE_USAGE_PATH", path):
                self.assertEqual(azure_tts.usage(), 300)
                azure_tts.record(7, "test")
                self.assertEqual(azure_tts.usage(), 307)
        finally:
            os.remove(path)

    def test_billing_and_document(self):
        body = '<phoneme alphabet="ipa" ph="ˈhæ">Ha</phoneme>'
        self.assertEqual(azure_tts.billable(body), len(body))
        doc = azure_tts.document(body, "en-US-AndrewNeural")
        self.assertIn('xml:lang="en-US"', doc)
        self.assertIn(f'<voice name="en-US-AndrewNeural">{body}</voice>', doc)
        self.assertEqual(azure_tts.wrap_rate(body, 0), body)

    def test_which_errors_stop_a_render(self):
        self.assertFalse(azure_tts._http_error(400, "").fatal)
        for status in (401, 403, 429, 503):
            self.assertTrue(azure_tts._http_error(status, "").fatal, status)

    def test_region_takes_the_endpoint_form(self):
        with mock.patch.dict(os.environ, {azure_tts.KEY_ENV: "k",
                                          azure_tts.REGION_ENV: " East US "}):
            self.assertEqual(azure_tts.settings(), ("k", "eastus"))

    def _synthesize_with(self, post):
        """azure_tts.synthesize with _post replaced, no waiting, a scratch
        ledger and output file; returns (result or exception, ledger chars)."""
        fd, ledger = tempfile.mkstemp(suffix=".jsonl")
        os.close(fd)
        out = ledger + ".mp3"
        env = {azure_tts.KEY_ENV: "k", azure_tts.REGION_ENV: "eastus"}
        try:
            with mock.patch.dict(os.environ, env), \
                    mock.patch.object(config, "AZURE_USAGE_PATH", ledger), \
                    mock.patch.object(azure_tts, "_post", side_effect=post), \
                    mock.patch.object(azure_tts.time, "sleep"), \
                    mock.patch.object(azure_tts, "MIN_INTERVAL", 0):
                try:
                    result = azure_tts.synthesize("Hello there.", "en-US-AndrewNeural", out)
                except azure_tts.AzureError as e:
                    result = e
                return result, azure_tts.usage()
        finally:
            for p in (ledger, out):
                if os.path.exists(p):
                    os.remove(p)

    def test_a_cut_off_answer_is_retried_once_then_fatal(self):
        import http.client
        calls = []

        def post(ssml, key, region, billed):
            calls.append(1)
            billed()
            raise http.client.IncompleteRead(b"")
        result, used = self._synthesize_with(post)
        self.assertIsInstance(result, azure_tts.AzureError)
        self.assertTrue(result.fatal)
        self.assertEqual(len(calls), 2)
        self.assertEqual(used, 2 * len("Hello there."))   # both were billed

    def test_an_answer_too_short_is_still_logged(self):
        def post(ssml, key, region, billed):
            billed()
            return b"x" * 10
        result, used = self._synthesize_with(post)
        self.assertIsInstance(result, azure_tts.AzureError)
        self.assertFalse(result.fatal)
        self.assertEqual(used, len("Hello there."))

    def test_success_writes_the_file_and_logs_it(self):
        def post(ssml, key, region, billed):
            self.assertIn("<voice name=\"en-US-AndrewNeural\">Hello there.</voice>", ssml)
            billed()
            return b"\xff" * 2000
        result, used = self._synthesize_with(post)
        self.assertEqual(result, len("Hello there."))
        self.assertEqual(used, len("Hello there."))

    def test_no_key_is_fatal_before_any_request(self):
        env = {k: v for k, v in os.environ.items()
               if k not in (azure_tts.KEY_ENV, azure_tts.REGION_ENV)}
        with mock.patch.dict(os.environ, env, clear=True), \
                mock.patch.object(azure_tts, "_post") as post:
            with self.assertRaises(azure_tts.AzureError) as cm:
                azure_tts.synthesize("Hi", "en-US-AndrewNeural", "unused.mp3")
            self.assertTrue(cm.exception.fatal)
            post.assert_not_called()


class SavedForm(unittest.TestCase):
    def test_use_ipa_is_written_only_when_on(self):
        on = pronunciation._tidy({"say": "x", "override": False, "use_ipa": True})
        off = pronunciation._tidy({"say": "x", "override": False, "use_ipa": False})
        self.assertIs(on["use_ipa"], True)
        self.assertNotIn("use_ipa", off)
        self.assertEqual(list(on), ["say", "override", "use_ipa"])

    def test_use_ipa_false_is_not_an_edit(self):
        self.assertEqual(pronunciation._canon({"say": "x", "use_ipa": False}),
                         pronunciation._canon({"say": "x"}))

    def test_use_ipa_alone_reads_as_fixed(self):
        self.assertEqual(pronunciation.status_of({"use_ipa": True}),
                         pronunciation.STATUS_FIXED)


class EdgeRetry(unittest.TestCase):
    """tts_engine.synthesize against a stand-in edge-tts: an empty answer is
    asked again, an unreachable service is not."""

    def setUp(self):
        cache = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, cache, True)
        for patcher in (mock.patch.object(tts_engine, "AUDIO_CACHE_DIR", cache),
                        mock.patch.object(tts_engine, "_edge_down_until", 0.0),
                        mock.patch.object(tts_engine.time, "sleep"),
                        mock.patch.object(tts_engine, "_synthesize_sapi",
                                          side_effect=self.sapi)):
            patcher.start()
            self.addCleanup(patcher.stop)

    @staticmethod
    def sapi(text, rate, out_path):
        with open(out_path, "wb") as f:
            f.write(b"w" * 600)

    def speak(self, answers):
        """Synthesize a plain verse while edge gives ``answers`` in turn: an
        exception to raise, or None for audio. Returns (path, edge calls)."""
        import edge_tts
        calls = []

        class Communicate:
            def __init__(self, **kwargs):
                pass

            async def save(self, out_path):
                calls.append(out_path)
                if answers[len(calls) - 1] is not None:
                    raise answers[len(calls) - 1]
                with open(out_path, "wb") as f:
                    f.write(b"x" * 600)

        with mock.patch.object(edge_tts, "Communicate", Communicate):
            path = tts_engine.synthesize("And the border turned about westward.",
                                         tts_engine.HOUSE_VOICE, 0)
        return path, len(calls)

    @staticmethod
    def empty():
        from edge_tts.exceptions import NoAudioReceived
        return NoAudioReceived("No audio was received.")

    def test_an_empty_answer_is_asked_again(self):
        path, calls = self.speak([self.empty(), None])
        self.assertTrue(path.endswith(".mp3"))
        self.assertEqual(calls, 2)
        self.assertEqual(tts_engine._edge_down_until, 0.0)    # not counted as down

    def test_edge_is_down_once_the_retries_run_out(self):
        tries = len(tts_engine._EDGE_EMPTY_WAITS) + 1
        path, calls = self.speak([self.empty()] * tries)
        self.assertTrue(path.endswith(".wav"))
        self.assertEqual(calls, tries)
        self.assertGreater(tts_engine._edge_down_until, 0.0)

    def test_an_unreachable_edge_is_not_asked_again(self):
        path, calls = self.speak([OSError("unreachable")])
        self.assertTrue(path.endswith(".wav"))
        self.assertEqual(calls, 1)


if __name__ == "__main__":
    unittest.main()
