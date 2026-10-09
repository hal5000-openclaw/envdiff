import contextlib, io, json, os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import envdiff


def run(a, b, *flags):
    with tempfile.TemporaryDirectory() as d:
        pa, pb = os.path.join(d, "a"), os.path.join(d, "b")
        open(pa, "w").write(a)
        open(pb, "w").write(b)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = envdiff.main([pa, pb, *flags])
    return code, out.getvalue()


class T(unittest.TestCase):
    def test_comments_blank(self):
        self.assertEqual(envdiff.parse("# c\n\nA=1\n"), {"A": "1"})

    def test_export(self):
        self.assertEqual(envdiff.parse("export A=1"), {"A": "1"})

    def test_quotes(self):
        self.assertEqual(envdiff.parse("A=\"x y\"\nB='z'"), {"A": "x y", "B": "z"})

    def test_inline_comment(self):
        self.assertEqual(envdiff.parse("A=1 # hi"), {"A": "1"})

    def test_identical(self):
        code, out = run("A=1\n", "export A='1'\n")
        self.assertEqual(code, 0)

    def test_missing_and_diff_masked(self):
        code, out = run("A=1\nB=secret\n", "B=other\nC=3\n")
        self.assertEqual(code, 1)
        self.assertIn("A", out)
        self.assertIn("C", out)
        self.assertNotIn("secret", out)

    def test_show_values(self):
        _, out = run("B=secret\n", "B=other\n", "--show-values")
        self.assertIn("secret", out)

    def test_json(self):
        code, out = run("A=1\n", "B=2\n", "--json")
        d = json.loads(out)
        self.assertEqual(d["missing_in_b"], ["A"])
        self.assertEqual(d["missing_in_a"], ["B"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
