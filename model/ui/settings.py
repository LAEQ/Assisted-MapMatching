
class Settings:

    def __init__(self,_dlg):
        self.dlg = _dlg
        self.settings = {}


    def update_settings(self) -> None:

        self.settings["combo_network"] = self.dlg.combo_network.currentText()
        self.settings["combo_path"] = self.dlg.combo_path.currentText()
        self.settings["combo_oid"] = self.dlg.combo_oid.currentText()
        self.settings["combo_speed"] = self.dlg.combo_speed.currentText()
        self.settings["check_speed"] = self.dlg.check_speed.isChecked()

        self.settings["spin_buffer_range"] = self.dlg.spin_buffer_range.value()

        self.settings["combo_algo_matching"] = self.dlg.combo_algo_matching.currentText()

        
        self.settings["spin_stop_speed"] = self.dlg.spin_stop_speed.value()

        self.settings["spin_close_call"] = self.dlg.spin_close_call.value()
        self.settings["spin_intersection"] = self.dlg.spin_intersection.value()

        self.settings["spin_searching_radius"] = self.dlg.spin_searching_radius.value()
        self.settings["spin_sigma"] = self.dlg.spin_sigma.value()

        self.settings["combo_format"] = self.dlg.combo_format.currentText()
        self.settings["check_initial_path"] = self.dlg.check_initial_path.isChecked()
        self.settings["check_polyline"] = self.dlg.check_polyline.isChecked()
        self.settings["check_corrected_network"] = self.dlg.check_corrected_network.isChecked()
        self.settings["check_matched_path"] = self.dlg.check_matched_path.isChecked()

    def get_settings(self) -> dict:
        self.update_settings()
        return self.settings
