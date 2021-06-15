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
        <translation>Assisted-MapMatching</translation>
    </message>

    <message>
        <source>q3m.toolbar.title</source>
        <translation>Assisted-MapMatching</translation>
    </message>

    <message>
        <source>q3m.window.btn.import.test.set</source>
        <translation >Demo dataset</translation>
    </message>

    <message>
        <source>q3m.window.tab.main</source>
        <translation >Process</translation>
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
        <translation >Step 1: Data preparation</translation>
    </message>

    <message>
        <source>q3m.window.label.network</source>
        <translation >Street network layer</translation>
    </message>

    <message>
        <source>q3m.window.label.path</source>
        <translation >GPS trace layer</translation>
    </message>

    <message>
        <source>q3m.window.label.oid</source>
        <translation >Point identifier field</translation>
    </message>

    <message>
        <source>q3m.window.label.speed</source>
        <translation >Speed field</translation>
    </message>

    <message>
        <source>q3m.window.label.buffer_range</source>
        <translation >Buffer size [m]</translation>
    </message>

    <message>
        <source>q3m.window.btn.reload.layers</source>
        <translation >Reload</translation>
    </message>

    <message>
        <source>q3m.window.btn.reduce.network</source>
        <translation >Reduce network</translation>
    </message>

    <message>
        <source>q3m.window.btn.correct.topology</source>
        <translation >Correct Topology</translation>
    </message>


    <!-- Matching group -->


    <message>
        <source>q3m.window.group.matching</source>
        <translation >Step 2: MapMatching</translation>
    </message>

    <message>
        <source>q3m.window.distance_matching</source>
        <translation >by distance</translation>
    </message>

    <message>
        <source>q3m.window.speed_matching</source>
        <translation >by speed</translation>
    </message>
    
    <message>
        <source>q3m.window.closest_matching</source>
        <translation >to closest</translation>
    </message>

    <message>
        <source>q3m.window.btn.map.matching</source>
        <translation >Pre-MapMatching</translation>
    </message>

    <message>
        <source>q3m.window.btn.reselect.path</source>
        <translation >Reselect the path</translation>
    </message>

    <message>
        <source>q3m.window.btn.apply.path.change</source>
        <translation >Apply modifications to matched points</translation>
    </message>


    <!-- Export group -->


    <message>
        <source>q3m.window.group.export</source>
        <translation >Step 3: Export</translation>
    </message>

    <message>
        <source>q3m.window.btn.export.matched.track</source>
        <translation >Export the results</translation>
    </message>

    <message>
        <source>q3m.window.btn.export.polyline</source>
        <translation >Export the polyline</translation>
    </message>

    <message>
        <source>q3m.window.btn.export.project</source>
        <translation >Export the project</translation>
    </message>

    <message>
        <source>q3m.window.btn.reset</source>
        <translation >Reset</translation>
    </message>


    <!-- Panel 2: settings -->


    <message>
        <source>q3m.window.label.speed_limit</source>
        <translation >Stop speed threshold</translation>
    </message>


    <!-- Topology group -->


    <message>
        <source>q3m.window.group.topology.settings</source>
        <translation >Topological tolerance</translation>  
    </message>

    <message>
        <source>q3m.window.label.close_call</source>
        <translation >Close call tolerance</translation> <!--A retirer: une histoire de threshold ici de mémoire-->
    </message>

    <message>
        <source>q3m.window.label.intersection</source>
        <translation >Intersections and Dangle Nodes tolerance</translation> <!--A retirer: une histoire de threshold ici de mémoire-->
    </message>


    <!-- Matching group -->


    <message>
        <source>q3m.window.group.matching.settings</source>
        <translation >MapMatching tolerance</translation>
    </message>

    <message>
        <source>q3m.window.label.searching_radius</source>
        <translation >Searching distance</translation>
    </message>

    <message>
        <source>q3m.window.label.sigma</source>
        <translation >Sigma</translation>
    </message>


    <!-- Export group -->


    <message>
        <source>q3m.window.group.export.settings</source>
        <translation >Configuration for the export</translation>
    </message>

    <message>
        <source>q3m.window.label.format</source>
        <translation >Format</translation>
    </message>

    <message>
        <source>q3m.window.check.initial.path</source>
        <translation >Original GPS trace</translation>
    </message>

    <message>
        <source>q3m.window.check.polyline</source>
        <translation >Polyline</translation>
    </message>

    <message>
        <source>q3m.window.check.corrected.network</source>
        <translation >Corrected street network</translation>
    </message>

    <message>
        <source>q3m.window.check.matched.path</source>
        <translation >Matched GPS track</translation>
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
        <translation >There is an error with the import of librairies shapely or processing. Please check the documentation for further informations.</translation>
    </message>


    <!-- ******************* Map_matching.py error message******************** -->


    <!-- has_removed -->


    <message>
        <source>q3m.error.pre_algo_layer_deletion</source>
        <translation >Please refresh the layers to avoid errors</translation>
    </message>

    <message>
        <source>q3m.error.post_algo_layer_deletion</source>
        <translation >Don't delete layers during the process. Please reset the plugin for a fresh start.</translation>
    </message>


    <!-- on_click_reduce_network -->


    <message>
        <source>q3m.error.missing_input</source>
        <translation >One of the fields is empty. Please import a layer of type Point or LineString</translation>
    </message>

    <message>
        <source>q3m.error.can't_find_layer</source>
        <translation >Couldn't find one of the layers. Please reload the combobox and try again</translation>
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
        <translation >No layer detected. One should appear automatically after the pre-matching process</translation>
    </message>

    <message>
        <source>q3m.error.can't_export</source>
        <translation >A bug occurred during the exportation of the layer</translation>
    </message>

    <message>
        <source>q3m.error.nothing_to_export</source>
        <translation >There is nothing to export. Please check at least one of the exportation parameters in the second tab</translation>
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
        <translation >Can't select the path on the network: it hasn't been created yet</translation>
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
        <translation >The parameter speed limit can't be lower than 0</translation>
    </message>

    <message>
        <source>q3m.error.snap_points_along_line</source>
        <translation >A bug happened during the matching by speed</translation>
    </message>

    <message>
        <source>q3m.error.empty_layer</source>
        <translation >The layer used for this algorithm is empty</translation>
    </message>

    <message>
        <source>q3m.error.point_out_of_range</source>
        <translation >Parts of the points have been matched out of the range given in the parameters. Number of points: </translation>
    </message>


    <!-- ******************* Matcheur.py error message******************** -->


    <message>
        <source>q3m.error.error_searching_radius</source>
        <translation >The searching radius given in the parameters is too small</translation>
    </message>

    <message>
        <source>q3m.error.error_sigma</source>
        <translation >The sigma given in the parameters is too small</translation>
    </message>

    <message>
        <source>q3m.error.error_build_graph</source>
        <translation >There is an error inside the function build_graph</translation>
    </message>

    <message>
        <source>q3m.error.empty_best_path</source>
        <translation >Couldn't find the best path. Please increase the searching radius or sigma</translation>
    </message>

    <message>
        <source>q3m.error.empty_polyline</source>
        <translation >Couldn't build the polyline. Please increase the searching radius or sigma</translation>
    </message>

    <message>
        <source>q3m.error.distance_matcher</source>
        <translation >An error happened because of the library Leuvenmapmatching</translation>
    </message>


    <!-- ******************* LayerTraductor.py error message******************** -->
    
    
    <message>
        <source>q3m.error.not_a_layer</source>
        <translation >The parameter passed to this function isn't a QgsVectorLayer</translation>
    </message>
    
    <message>
        <source>q3m.error.not_a_list</source>
        <translation >The parameter passed to this function isn't a list</translation>
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
        <translation >No entity found in the given radius</translation>
    </message>

    <message>
        <source>q3m.error.empty_list</source>
        <translation >One of the parameters of the function is invalid: A list is empty</translation>
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
