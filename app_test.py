#!venv/bin/python
import unittest

from app import app


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.app = app.test_client()

    def tearDown(self):
        pass

    def login(self, username, password):
        return self.app.post('/login', data={
            'username': username,
            'password': password
            }, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


class CommonTest(TestCase):
    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Стартовая', rv.get_data(as_text=True))

    def test_wrong_login(self):
        rv = self.login('admin', 'admin')
        self.assertIn('Invalid', rv.get_data(as_text=True))

    def test_login_logout(self):
        rv = self.login('sd', 'Zen21atx')
        self.assertIn('<li>sd</li>', rv.get_data(as_text=True))
        rv = self.logout()
        self.assertIn('Стартовая', rv.get_data(as_text=True))


class AliasTest(TestCase):
    def test_alias_search_page(self):
        rv = self.app.get('/alias', follow_redirects=True)
        form = "<form class=\"form-search\" action=\"\" method=\"post\" name=\"search\">"
        self.assertIn(form, rv.get_data(as_text=True))

    def test_right_alias_search(self):
        aliases = ['test.intranet'+str(x) for x in range(1, 5)]
        rv = self.app.post('/alias/', data={'search': "test*"})
        self.assertIn('Вы искали &#39;test*&#39', rv.get_data(as_text=True))
        self.assertTrue(all(al in rv.get_data(as_text=True) for al in aliases))

    def test_wrong_alias_search(self):
        rv = self.app.post('/alias/', data={'search': "curly"})
        self.assertIn('Вы искали &#39;curly&#39', rv.get_data(as_text=True))
        self.assertIn('Ничего не найдено', rv.get_data(as_text=True))

    def test_right_alias_page(self):
        rv = self.app.get('/alias/tester')
        self.assertIn('/alias/tester/edit', rv.get_data(as_text=True))

    def test_wrong_alias_page(self):
        rv = self.app.get('/alias/curly', follow_redirects=True)
        self.assertIn('&#39;curly&#39; не существует', rv.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
