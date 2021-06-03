<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS><TS version="2.0">
<context>
    <name>MapMatching</name>

    <!-- *************************************************************************** -->
    <!-- *************************Interface Graphique******************************* -->
    <!-- *************************************************************************** -->

    <!-- Help File -->


    <message>
        <source>q3m.window.help_file</source>
        <translation>help_en.html</translation>
    </message>

    <message>
        <source>q3m.window.help_settings_file</source>
        <translation>help_settings_en.html</translation>
    </message>


    <!-- Header -->


    <message>
        <source>q3m.window.title</source>
        <translation>LAEQ-MapMatching</translation>
    </message>

    <message>
        <source>q3m.toolbar.title</source>
        <translation>MapMatching</translation>
    </message>

    <message>
        <source>q3m.window.label.subtitle</source>
        <translation >LAEQ Map Matching</translation>
    </message>

    <message>
        <source>q3m.window.tab.main</source>
        <translation >Matching</translation>
    </message>

    <message>
        <source>q3m.window.tab.settings</source>
        <translation >Settings</translation>
    </message>

    <message>
        <source>file_explorer_name</source>
        <translation >Save the layer as</translation>
    </message>


    <!-- Input group -->


    <message>
        <source>q3m.window.group.input</source>
        <translation >Step 1 : Input</translation>
    </message>

    <message>
        <source>q3m.window.label.network</source>
        <translation >Network layer</translation>
    </message>

    <message>
        <source>q3m.window.label.path</source>
        <translation >GPS Trace layer</translation>
    </message>

    <message>
        <source>q3m.window.label.oid</source>
        <translation >OID</translation>
    </message>

    <message>
        <source>q3m.window.label.speed</source>
        <translation >Speed</translation>
    </message>

    <message>
        <source>q3m.window.label.buffer_range</source>
        <translation >Buffer range [m]</translation>
    </message>

    <message>
        <source>q3m.window.btn.reload.layers</source>
        <translation >Reload</translation>
    </message>

    <message>
        <source>q3m.window.btn.reduce.network</source>
        <translation >Reduce the network</translation>
    </message>

    <message>
        <source>q3m.window.btn.correct.topology</source>
        <translation >Correct the topology</translation>
    </message>


    <!-- Matching group -->


    <message>
        <source>q3m.window.group.matching</source>
        <translation >Step 2 : Matching</translation>
    </message>

    <message>
        <source>q3m.window.distance_matching</source>
        <translation >Matching by distance</translation>
    </message>

    <message>
        <source>q3m.window.speed_matching</source>
        <translation >Matching with speed</translation>
    </message>
    
    <message>
        <source>q3m.window.closest_matching</source>
        <translation >Matching to closest</translation>
    </message>

    <message>
        <source>q3m.window.btn.map.matching</source>
        <translation >PreMatching</translation>
    </message>

    <message>
        <source>q3m.window.btn.reselect.path</source>
        <translation >Reselect path</translation>
    </message>

    <message>
        <source>q3m.window.btn.apply.path.change</source>
        <translation >Apply modification to path</translation>
    </message>


    <!-- Export group -->


    <message>
        <source>q3m.window.group.export</source>
        <translation >Step 3 : Export</translation>
    </message>

    <message>
        <source>q3m.window.btn.export.matched.track</source>
        <translation >Export matched trace</translation>
    </message>

    <message>
        <source>q3m.window.btn.export.polyline</source>
        <translation >Export polyline</translation>
    </message>

    <message>
        <source>q3m.window.btn.export.project</source>
        <translation >Export project</translation>
    </message>

    <message>
        <source>q3m.window.btn.reset</source>
        <translation >Reset</translation>
    </message>


    <!-- Panel 2: settings -->


    <message>
        <source>q3m.window.label.speed_limit</source>
        <translation >Speed stop limit</translation>
    </message>


    <!-- Topology group -->


    <message>
        <source>q3m.window.group.topology.settings</source>
        <translation >Topological tolerance</translation>
    </message>

    <message>
        <source>q3m.window.label.close_call</source>
        <translation >Close call</translation>
    </message>

    <message>
        <source>q3m.window.label.intersection</source>
        <translation >Intersection and Dangle Nodes</translation>
    </message>


    <!-- Matching group -->


    <message>
        <source>q3m.window.group.matching.settings</source>
        <translation >Matching tolerance</translation>
    </message>

    <message>
        <source>q3m.window.label.searching_radius</source>
        <translation >Searching radius</translation>
    </message>

    <message>
        <source>q3m.window.label.sigma</source>
        <translation >Sigma</translation>
    </message>


    <!-- Export group -->


    <message>
        <source>q3m.window.group.export.settings</source>
        <translation >Export config</translation>
    </message>

    <message>
        <source>q3m.window.label.format</source>
        <translation >Format</translation>
    </message>

    <message>
        <source>q3m.window.check.initial.path</source>
        <translation >Initial GPS trace</translation>
    </message>

    <message>
        <source>q3m.window.check.polyline</source>
        <translation >Polyline</translation>
    </message>

    <message>
        <source>q3m.window.check.corrected.network</source>
        <translation >Corrected network</translation>
    </message>

    <message>
        <source>q3m.window.check.matched.path</source>
        <translation >Matched trace</translation>
    </message>


    <!-- *************************************************************************** -->
    <!-- *************************Messages d'erreurs******************************** -->
    <!-- *************************************************************************** -->


    <message>
        <source>q3m.error.test</source>
        <translation >The test is working</translation>
    </message>

    <message>
        <source>q3m.error.import</source>
        <translation >Il y a un problème avec les imports. Se référer à la documentation pour plus de détail sur l'erreur</translation>
    </message>


    <!-- ******************* Map_matching.py error message******************** -->


    <!-- has_removed -->


    <message>
        <source>q3m.error.pre_algo_layer_deletion</source>
        <translation >Please click on RELOAD to avoid non existing values inside of the comboBox</translation>
    </message>

    <message>
        <source>q3m.error.post_algo_layer_deletion</source>
        <translation >Don't delete layers in the middle of the process, it will cause crash Please start again by pressing RESET.</translation>
    </message>


    <!-- on_click_reduce_network -->


    <message>
        <source>q3m.error.missing_input</source>
        <translation >One of the comboBox is empty. Please fill it by importing a layer of type Point or LineString</translation>
    </message>

    <message>
        <source>q3m.error.can't_find_layer</source>
        <translation >Couldn't find one of the layer inside the boxes. Please click on RELOAD to remove unexisting layer and start again</translation>
    </message>

    <message>
        <source>q3m.error.invalid_layer</source>
        <translation >One of your layers has a problem. Please check their projection system. Check the documentation for more detailed information</translation>
    </message>


    <!-- on_click_correct_topology -->


    <message>
        <source>q3m.error.no_layer</source>
        <translation >The core class: Layers hasn't been created. To correct this problem: Reset the plugin and reduce the network layer</translation>
    </message>


    <!-- export part -->


    <message>
        <source>q3m.error.no_matched_layer</source>
        <translation >No layer detected. One should appear automaticaly after the prematching process</translation>
    </message>

    <message>
        <source>q3m.error.can't_export</source>
        <translation >A bug occured during the exportation of the layer</translation>
    </message>

    <message>
        <source>q3m.error.nothing_to_export</source>
        <translation >There is nothing to export. Please check at least one of the exportation parameters present in the second tab</translation>
    </message>


    <!-- ******************* Network.py error message******************** -->


    <message>
        <source>q3m.error.processing</source>
        <translation >There is a problem with processing: please check if it is activated on your plateform (->Python console: import processing)</translation>
    </message>

    <message>
        <source>q3m.error.empty_attribute_name</source>
        <translation >No name given to create a new column inside the temporary layer</translation>
    </message>

    <message>
        <source>q3m.error.no_path_registered</source>
        <translation >Can't select in QGIS the path taken by the user: it hasn't been calculated yet</translation>
    </message>

    <message>
        <source>q3m.error.no_selection</source>
        <translation >No selection detected on the network layer</translation>
    </message>


    <!-- ******************* Path.py error message******************** -->


    <message>
        <source>q3m.error.buffer_range</source>
        <translation >The buffer range is too small</translation>
    </message>

    <message>
        <source>q3m.error.wrong_speed_column</source>
        <translation >Can't find the given field inside the path layer </translation>
    </message>

    <message>
        <source>q3m.error.negative_speed_limit</source>
        <translation >The speed limit given in the parameter can't be lower than 0</translation>
    </message>

    <message>
        <source>q3m.error.snap_points_along_line</source>
        <translation >A bug happened during the speed matching</translation>
    </message>

    <message>
        <source>q3m.error.empty_layer</source>
        <translation >The layer used for this algorithm is empty</translation>
    </message>

    <message>
        <source>q3m.error.point_out_of_range</source>
        <translation >A part of the points have been matched out of the range given in the parameters. Number of points :</translation>
    </message>


    <!-- ******************* Matcheur.py error message******************** -->


    <message>
        <source>q3m.error.error_searching_radius</source>
        <translation >The searching radius given in the parameters is too small</translation>
    </message>

    <message>
        <source>q3m.error.error_sigma</source>
        <translation >The sigma given in parameter is too small</translation>
    </message>

    <message>
        <source>q3m.error.error_build_graph</source>
        <translation >There is an error inside the function build_graph</translation>
    </message>

    <message>
        <source>q3m.error.empty_best_path</source>
        <translation >Couldn't find the best path. Please increase the searching radius </translation>
    </message>

    <message>
        <source>q3m.error.empty_polyline</source>
        <translation >Couldn't build the polyline. Please increase the searching radius</translation>
    </message>

    <message>
        <source>q3m.error.distance_matcher</source>
        <translation >An error happened because of the librairy Leuvenmapmatching</translation>
    </message>


    <!-- ******************* LayerTraductor.py error message******************** -->
    
    
    <message>
        <source>q3m.error.not_a_layer</source>
        <translation >The parameter of this function isn't a QgsVectorLayer</translation>
    </message>
    
    <message>
        <source>q3m.error.not_a_list</source>
        <translation >The parameter of this function isn't a list</translation>
    </message>

    <message>
        <source>q3m.error.conversion_error</source>
        <translation >Problem during the geometries conversion. The issue come from the encoding system</translation>
    </message>

    <message>
        <source>q3m.error.wrong_oid_column</source>
        <translation >Can't find the value of the OID column in the network layer</translation>
    </message>


    <!-- ******************* Geometry.py error message******************** -->


    <message>
        <source>q3m.error.invalid_input</source>
        <translation >A parameter of the function is empty/wrong</translation>
    </message>

    <message>
        <source>q3m.error.no_candidate_found</source>
        <translation >No entity found in the radius given</translation>
    </message>

    <message>
        <source>q3m.error.empty_list</source>
        <translation >One of the parameters of the function made an error: A list is empty</translation>
    </message>

</context>
<context>
    <name>UnitTest</name>
    <message>
        <location filename="../test/test_translations.py" line="45"/>
        <source>q3m.window.title</source>
        <translation>Mock window title</translation>
    </message>
</context>
</TS>
