import os, tempfile, unittest, io, contextlib
import envdiff as e


class T(unittest.TestCase):
    def test_parse(self):
        d = e.parse("# c\n\nexport A=1\nB='x y'\nC=\"z\"\nD=v # note\n")
        self.assertEqual(d, {"A": "1", "B": "x y", "C": "z", "D": "v"})

    def test_missing_and_diff(self):
        r = e.compare({"a": {"X": "1", "Y": "2"}, "b": {"X": "9"}})
        self.assertEqual(r["missing"], {"b": ["Y"]})
        self.assertEqual(list(r["differs"]), ["X"])

    def test_keys_only(self):
        r = e.compare({"a": {"X": "1"}, "b": {"X": "2"}}, keys_only=True)
        self.assertEqual(r, {"missing": {}, "differs": {}})

    def run_cli(self, a, b, *extra):
        with tempfile.TemporaryDirectory() as t:
            fa, fb = os.path.join(t, "a"), os.path.join(t, "b")
            open(fa, "w").write(a); open(fb, "w").write(b)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = e.main([fa, fb, *extra])
            return code, buf.getvalue()

    def test_exit_and_hiding(self):
        code, out = self.run_cli("K=alpha\n", "K=beta\n")
        self.assertEqual(code, 1)
        self.assertNotIn("alpha", out)
        code, out = self.run_cli("K=alpha\n", "K=beta\n", "--show-values")
        self.assertIn("alpha", out)

    def test_same(self):
        self.assertEqual(self.run_cli("K=1\n", "K=1\n")[0], 0)


if __name__ == "__main__":
    unittest.main()
