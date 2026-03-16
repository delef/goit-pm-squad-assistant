from ui import suggest_command


class TestSuggestCommand:
    def test_close_match(self):
        assert suggest_command("ad") == "Invalid command. Did you mean: add?"

    def test_typo_in_compound_command(self):
        assert suggest_command("add-nore") == "Invalid command. Did you mean: add-note?"

    def test_no_match(self):
        assert suggest_command("xyzzy") == "Invalid command."

    def test_exact_prefix_typo(self):
        assert suggest_command("helo") == "Invalid command. Did you mean: hello?"

    def test_show_notes_typo(self):
        assert suggest_command("show-noets") == "Invalid command. Did you mean: show-notes?"

    def test_completely_unrelated(self):
        assert suggest_command("foobar") == "Invalid command."
