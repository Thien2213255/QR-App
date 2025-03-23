import qrcode
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from PIL import Image as PILImage
from plyer import filechooser

class QRCodeApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.url_input = TextInput(hint_text="Nhập link hoặc thông tin Wi-Fi...", multiline=False, size_hint=(1, 0.2))
        layout.add_widget(self.url_input)

        self.wifi_ssid = TextInput(hint_text="Tên Wi-Fi (SSID)", multiline=False, size_hint=(1, 0.2))
        layout.add_widget(self.wifi_ssid)

        self.wifi_password = TextInput(hint_text="Mật khẩu Wi-Fi", multiline=False, size_hint=(1, 0.2))
        layout.add_widget(self.wifi_password)

        generate_button = Button(text="Tạo QR Code", size_hint=(1, 0.2))
        generate_button.bind(on_press=self.generate_qr_code)
        layout.add_widget(generate_button)

        self.qr_image = Image(size_hint=(1, 0.6))
        layout.add_widget(self.qr_image)

        save_button = Button(text="Lưu QR Code", size_hint=(1, 0.2))
        save_button.bind(on_press=self.save_qr_code)
        layout.add_widget(save_button)

        self.qr = None  # Chỉ lưu QR code tạm, không lưu file sẵn
        return layout

    def generate_qr_code(self, instance):
        """Tạo QR Code từ URL hoặc thông tin Wi-Fi nhưng KHÔNG lưu file sẵn."""
        url = self.url_input.text.strip()
        ssid = self.wifi_ssid.text.strip()
        password = self.wifi_password.text.strip()

        if ssid and password:
            qr_data = f"WIFI:S:{ssid};T:WPA;P:{password};;"
        elif url:
            qr_data = url
        else:
            print("LỖI: Không có dữ liệu để tạo QR Code.")
            return

        self.qr = qrcode.make(qr_data)  # Tạo QR code nhưng không lưu file
        self.display_qr()

    def display_qr(self):
        """Hiển thị QR Code lên giao diện."""
        if self.qr:
            pil_image = self.qr.convert("RGBA")
            data = pil_image.tobytes()

            texture = Texture.create(size=pil_image.size, colorfmt="rgba")
            texture.blit_buffer(data, colorfmt="rgba", bufferfmt="ubyte")
            self.qr_image.texture = texture

    def save_qr_code(self, instance):
        """Mở hộp thoại để người dùng chọn nơi lưu QR Code."""
        if self.qr is None:
            print("LỖI: Chưa có QR Code để lưu!")
            return

        file_path = filechooser.save_file(title="Chọn nơi lưu QR Code", filters=[("PNG files", "*.png")])
        if not file_path:
            print("Không có tên file nào được nhập.")
            return
        if file_path and isinstance(file_path, list):
            file_path = file_path[0]  # Lấy đường dẫn đầu tiên nếu có nhiều kết quả
        if not file_path.endswith(".png"):
            file_path += ".png"

        self.qr.save(file_path)
        print(f"✅ QR Code đã được lưu tại: {file_path}")


if __name__ == "__main__":
    QRCodeApp().run()
