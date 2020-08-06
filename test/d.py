import unittest
from selenium import webdriver
from time import sleep

class LoginCase(unittest.TestCase):

    def setUp(self):
        self.dr=webdriver.Chrome()
        self.dr.maximize_window()

    def login(self,username,password):
        self.dr.get('https://passport.cnblogs.com/user/signin')#cnblog登录页面
        self.dr.find_element_by_id('input1').send_keys(username)
        self.dr.find_element_by_id('input2').send_keys(password)
        self.dr.find_element_by_id('signin').click()

    def test_login_success(self):
        '''用户名、密码正确'''
        self.login('你很甜！','ccccc')
        sleep(3)
        link=self.dr.find_element_by_xpath('//*[@id="captchaBox"]/div/div[2]/div[1]/div[1]/div[1]')
        #self.assertTrue('你很甜！' in link.text)#用assertTrue(x)方法来断言bool(x) is True 登陆成功后用户昵称在link_curren_user里
        self.dr.find_element_by_xpath("//*[@id=\"captchaBox\"]/div/div[3]").click()
        self.dr.get_screenshot_as_file('D://cnblogtest//login_success.png')#截图，可自定义截图后的保存位置和图片命名

    def test_login_pwd_null(self):
        '''用户名正确，密码不正确'''
        self.login('xxx','111')
        sleep(2)
        error_message=self.dr.find_element_by_id('tip_btn').text
        self.assertIn('用户名或密码错误',error_message)
        self.dr.get_screenshot_as_file('D://cnblogtest//login_pwd_error.png')

    def test_login_pwd_null(self):
        '''用户名正确，密码为空'''
        self.login('xxx','')
        error_message=self.dr.find_element_by_id('tip_input2').text
        self.assertEqual(error_message,'请输入密码')
        self.dr.get_screenshot_as_file('D://cnblogtest//login_pwd_null.png')

    def test_login_user_error(self):
        '''用户名错误，密码正确'''
        self.login('wwc','xxxxxx')
        sleep(2)
        error_message=self.dr.find_element_by_id('tip_btn').text
        self.assertIn('该用户不存在',error_message)
        self.dr.get_screenshot_as_file('D://cnblogtest//login_user_error.png')

    def test_login_user_null(self):
        '''用户名为空，密码正确'''
        self.login('','cccccc')
        error_message=self.dr.find_element_by_id('tip_input1').text
        self.assertEqual(error_message,'请输入登录用户名')
        self.dr.get_screenshot_as_file('D://cnblogtest//login_user_null.png')

    def tearDown(self):
        sleep(2)
        print('自动测试完毕！')
        self.dr.quit()

if __name__ == '__main__':
    unittest.main()
11