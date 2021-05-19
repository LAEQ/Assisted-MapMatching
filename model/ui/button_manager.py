

class Button_manager():

    def __init__(self,_dlg) -> None:
        self.dlg = _dlg


    def __disable_all_buttons(self) -> None:
        """Disable every elements of the plugin. """

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

        self.dlg.combo_matched_track.setEnabled(False)
        self.dlg.btn_export_matched_track.setEnabled(False)
        self.dlg.btn_export_polyline.setEnabled(False)
        self.dlg.btn_export_project.setEnabled(False)



    def set_input_state_buttons(self) -> None:
        """Activate every buttons related to the network reduction"""

        self.__disable_all_buttons()

        self.dlg.combo_network.setEnabled(True)
        self.dlg.combo_path.setEnabled(True)
        self.dlg.combo_oid.setEnabled(True)
        self.dlg.btn_reload_layers.setEnabled(True)

        self.dlg.spin_buffer_range.setEnabled(True)
        self.dlg.btn_reduce_network.setEnabled(True)


    def set_topology_state_buttons(self) -> None:
        """Activate every buttons related to topological operations"""

        self.set_input_state_buttons()
        self.dlg.btn_correct_topology.setEnabled(True)


    def set_pre_matching_state_buttons(self):
        """ Activate every buttons related to the 
            pre-mapMatching operation
        """
        
        self.__disable_all_buttons()

        self.dlg.combo_speed.setEnabled(True)
        self.dlg.check_speed.setEnabled(True)

        self.dlg.combo_algo_matching.setEnabled(True)
        self.dlg.btn_map_matching.setEnabled(True)


    def set_modification_state_buttons(self) -> None:
        """ Activate every buttons related to the 
            modification of the matched trace
        """

        self.__disable_all_buttons()

        self.dlg.combo_speed.setEnabled(True)
        self.dlg.check_speed.setEnabled(True)
           
        self.dlg.combo_algo_matching.setEnabled(True)
        self.dlg.btn_reselect_path.setEnabled(True)
        self.dlg.btn_apply_path_change.setEnabled(True)

        self.dlg.combo_matched_track.setEnabled(True)
        self.dlg.btn_export_matched_track.setEnabled(True)
        self.dlg.btn_export_polyline.setEnabled(True)
        self.dlg.btn_export_project.setEnabled(True)