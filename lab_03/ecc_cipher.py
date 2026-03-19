import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.ecc import Ui_Dialog


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Connect buttons
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    # ================== GENERATE KEYS ==================
    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/ecc/generate_keys"

        try:
            print(">>> Calling generate keys API...")
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                QMessageBox.information(
                    self,
                    "Success",
                    data.get("message", "Keys generated!")
                )
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Status code: {response.status_code}"
                )

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    # ================== SIGN ==================
    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/ecc/sign"

        message = self.ui.txtInformation.toPlainText()

        payload = {
            "message": message
        }

        try:
            print(">>> Calling sign API...")
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()

                signature = data.get("signature", "")
                self.ui.txtSignature.setText(signature)

                QMessageBox.information(
                    self, "Success", "Signed successfully!")

            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Status code: {response.status_code}"
                )

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    # ================== VERIFY ==================
    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/ecc/verify"

        message = self.ui.txtInformation.toPlainText()
        signature = self.ui.txtSignature.toPlainText()

        payload = {
            "message": message,
            "signature": signature
        }

        try:
            print(">>> Calling verify API...")
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()

                is_verified = data.get("is_verified", False)

                if is_verified:
                    QMessageBox.information(
                        self, "Result", "✅ Signature VALID")
                else:
                    QMessageBox.warning(self, "Result", "❌ Signature INVALID")

            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Status code: {response.status_code}"
                )

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", str(e))

def call_api_verify(self):
    url = "http://127.0.0.1:5000/api/ecc/verify"

    payload = {
        "message": self.ui.txtInformation.toPlainText(),
        "signature": self.ui.txtSignature.toPlainText()
    }

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()

            if data["is_verified"]:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Verified Successfully")
                msg.exec_()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Verified Fail")
                msg.exec_()
        else:
            print("Error while calling API")

    except requests.exceptions.RequestException as e:
        print("Error:", str(e))
# ================== MAIN ==================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
