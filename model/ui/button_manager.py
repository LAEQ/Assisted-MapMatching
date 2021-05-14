

class Button_manager():

    def __init__(self,_dlg) -> None:
        self.dlg = _dlg

    def disable_all_buttons(self):
           self.dlg.combo_network.setEnabled(False)
           self.dlg.combo_path.setEnabled(False)
           self.dlg.combo_oid.setEnabled(False)
           self.dlg.combo_speed.setEnabled(False)
           self.dlg.check_speed.setEnabled(False)
           self.dlg.btn_reload_layers.setEnabled(False)

           self.dlg.spin_buffer_range.setEnabled(False)
           self.dlg.btn_reduce_network.setEnabled(False)

           self.dlg.btn_correct_topology.setEnabled(False)

           self.dlg.combo_algo_matching.setEnabled(False)
           self.dlg.btn_map_matching.setEnabled(False)
           
           self.dlg.btn_reselect_path.setEnabled(False)
           self.dlg.btn_apply_path_change.setEnabled(False)

    def set_input_state_buttons(self):
        self.disable_all_buttons()

        self.dlg.combo_network.setEnabled(True)
        self.dlg.combo_path.setEnabled(True)
        self.dlg.combo_oid.setEnabled(True)
        self.dlg.btn_reload_layers.setEnabled(True)

        self.dlg.spin_buffer_range.setEnabled(True)
        self.dlg.btn_reduce_network.setEnabled(True)

    def set_topology_state_buttons(self):

        self.set_input_state_buttons()
        self.dlg.btn_correct_topology.setEnabled(True)

    def set_pre_matching_state_buttons(self):
        self.disable_all_buttons()

        self.dlg.combo_speed.setEnabled(True)
        self.dlg.check_speed.setEnabled(True)

        self.dlg.combo_algo_matching.setEnabled(True)
        self.dlg.btn_map_matching.setEnabled(True)

    def set_modification_state_buttons(self):
        self.disable_all_buttons()

        self.dlg.combo_speed.setEnabled(True)
        self.dlg.check_speed.setEnabled(True)
           
        self.dlg.combo_algo_matching.setEnabled(True)
        self.dlg.btn_reselect_path.setEnabled(True)
        self.dlg.btn_apply_path_change.setEnabled(True)

    def set_import_state(self):
        self.disable_all_buttons()
        #todo