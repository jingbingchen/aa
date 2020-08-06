from pzdf_base_test_case import PzdfBaseTestCase


class PzdfTestCase2(PzdfBaseTestCase):

    def test_100_phone(self):
        d = self.custom_device(self.param)
        d.app_start("com.android.pzPhone")
        d(resourceId="com.android.pzPhone:id/btn_phone_9").click()
        d(resourceId="com.android.pzPhone:id/btn_phone_1").click()
        d(resourceId="com.android.pzPhone:id/btn_phone_1").click()
        d(resourceId="com.android.pzPhone:id/btn_phone_3").click()
