<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS><TS version="2.0" language="fr" sourcelanguage="">
<context>
    <name>MapMatching</name>

    <!-- *************************************************************************** -->
    <!-- *************************Interface Graphique******************************* -->
    <!-- *************************************************************************** -->

    <!-- Help File -->


    <message>
        <source>q3m.window.help_file</source>
        <translation>help_fr.html</translation>
    </message>

    <message>
        <source>q3m.window.help_settings_file</source>
        <translation>help_settings_fr.html</translation>
    </message>


    <!-- Header -->


    <message>
        <source>q3m.window.title</source>
        <translation>LAEQ-CorrélationCartographique</translation>
    </message>

    <message>
        <source>q3m.toolbar.title</source>
        <translation>CorrélationCartographique</translation>
    </message>

    <message>
        <source>q3m.window.label.subtitle</source>
        <translation >Laeq Map-Matching</translation>
    </message>

    <message>
        <source>q3m.window.tab.main</source>
        <translation >Matcheur</translation>
    </message>
    
    <message>
        <source>q3m.window.tab.settings</source>
        <translation >Paramètres</translation>
    </message>

    <message>
        <source>file_explorer_name</source>
        <translation >Enregistrer la couche comme</translation>
    </message>


    <!-- Input group -->


    <message>
        <source>q3m.window.group.input</source>
        <translation >Etape 1 : Entrées</translation>
    </message>

    <message>
        <source>q3m.window.label.network</source>
        <translation >Couche réseau</translation>
    </message>

    <message>
        <source>q3m.window.label.path</source>
        <translation >Couche Trace GPS</translation>
    </message>

    <message>
        <source>q3m.window.label.oid</source>
        <translation >OID</translation>
    </message>

    <message>
        <source>q3m.window.label.speed</source>
        <translation >Vitesse</translation>
    </message>

    <message>
        <source>q3m.window.label.buffer_range</source>
        <translation >Taille du tampon [m]</translation>
    </message>

    <message>
        <source>q3m.window.btn.reload.layers</source>
        <translation >Reload</translation>
    </message>

    <message>
        <source>q3m.window.btn.reduce.network</source>
        <translation >Réduire la carte</translation>
    </message>

    <message>
        <source>q3m.window.btn.correct.topology</source>
        <translation >Corriger la topologie</translation>
    </message>


    <!-- Matching group -->


    <message>
        <source>q3m.window.group.matching</source>
        <translation >Etape 2 : Matching</translation>
    </message>

    <message>
        <source>q3m.window.distance_matching</source>
        <translation >Matcher par la distance</translation>
    </message>

    <message>
        <source>q3m.window.speed_matching</source>
        <translation >Matcher par vitesse</translation>
    </message>
    
    <message>
        <source>q3m.window.closest_matching</source>
        <translation >Matcher au plus près</translation>
    </message>

    <message>
        <source>q3m.window.btn.map.matching</source>
        <translation >Pre-Matching</translation>
    </message>

    <message>
        <source>q3m.window.btn.reselect.path</source>
        <translation >Re selectionner la route</translation>
    </message>

    <message>
        <source>q3m.window.btn.apply.path.change</source>
        <translation >Appliquer les modification</translation>
    </message>


    <!-- Export group -->


    <message>
        <source>q3m.window.group.export</source>
        <translation >Etape 3 : Export</translation>
    </message>

    <message>
        <source>q3m.window.btn.export.matched.track</source>
        <translation >Exporter la trace Matchée</translation>
    </message>

    <message>
        <source>q3m.window.btn.export.polyline</source>
        <translation >Exporter la polyline</translation>
    </message>

    <message>
        <source>q3m.window.btn.export.project</source>
        <translation >Exporter le projet</translation>
    </message>

    <message>
        <source>q3m.window.btn.reset</source>
        <translation >Reset</translation>
    </message>


    <!-- Panel 2: settings -->


    <message>
        <source>q3m.window.label.speed_limit</source>
        <translation >Limite de vitesse à l'arrêt</translation>
    </message>


    <!-- Topology group -->


    <message>
        <source>q3m.window.group.topology.settings</source>
        <translation >Tolérance topologique</translation>
    </message>

    <message>
        <source>q3m.window.label.close_call</source>
        <translation >Points proche</translation>
    </message>

    <message>
        <source>q3m.window.label.intersection</source>
        <translation >Intersection et Dangle Nodes</translation>
    </message>


    <!-- Matching group -->


    <message>
        <source>q3m.window.group.matching.settings</source>
        <translation >Tolérance de matching</translation>
    </message>

    <message>
        <source>q3m.window.label.searching_radius</source>
        <translation >Rayon de recherche</translation>
    </message>

    <message>
        <source>q3m.window.label.sigma</source>
        <translation >Sigma</translation>
    </message>


    <!-- Export group -->


    <message>
        <source>q3m.window.group.export.settings</source>
        <translation >Configuration de l'exportation</translation>
    </message>

    <message>
        <source>q3m.window.label.format</source>
        <translation >Format</translation>
    </message>

    <message>
        <source>q3m.window.check.initial.path</source>
        <translation >Trace GPS initial</translation>
    </message>

    <message>
        <source>q3m.window.check.polyline</source>
        <translation >Polyline</translation>
    </message>

    <message>
        <source>q3m.window.check.corrected.network</source>
        <translation >Réseau de routes corrigé</translation>
    </message>

    <message>
        <source>q3m.window.check.matched.path</source>
        <translation >Trace GPS matchée</translation>
    </message>


    <!-- *************************************************************************** -->
    <!-- *************************Messages d'erreurs******************************** -->
    <!-- *************************************************************************** -->


    <message>
        <source>q3m.error.test</source>
        <translation >Le test est fonctionnel</translation>
    </message>


    <!-- ******************* Map_matching.py error message******************** -->


    <!-- has_removed -->


    <message>
        <source>q3m.error.pre_algo_layer_deletion</source>
        <translation >Il est conseillé de cliquer sur RELOAD pour éviter d'avoir des valeurs désormais inexistante dans les comboBox</translation>
    </message>

    <message>
        <source>q3m.error.post_algo_layer_deletion</source>
        <translation >C'est jamais une bonne idée de supprimer des éléments au milieu du traitement. Appuyer sur RESET pour revenir à 0</translation>
    </message>


    <!-- on_click_reduce_network -->


    <message>
        <source>q3m.error.missing_input</source>
        <translation >Une des comboBox est vide. Merci de la remplir en important une couche de type point ou LineString</translation>
    </message>

    <message>
        <source>q3m.error.can't_find_layer</source>
        <translation >Impossible de trouver une des couches renseignés dans une des boites, essayer de cliquer sur reload pour supprimer les choix inexistant</translation>
    </message>

    <message>
        <source>q3m.error.invalid_layer</source>
        <translation >Une de vos couches présente une anomalie: vérifier leur système de projection. Se référer à la documentation pour plus d'explication</translation>
    </message>


    <!-- on_click_correct_topology -->


    <message>
        <source>q3m.error.no_layer</source>
        <translation >La classe mère du plugin: Layers n'a pas été instancié. Pour corriger ce problème: relancer le plugin et réduire la carte</translation>
    </message>


    <!-- export part -->


    <message>
        <source>q3m.error.no_matched_layer</source>
        <translation >Aucune couche matché détécté. Une couche devrait automatiquement apparaitre après avoir lancé le pré-matching</translation>
    </message>

    <message>
        <source>q3m.error.can't_export</source>
        <translation >Impossible d'exporter la couche</translation>
    </message>

    <message>
        <source>q3m.error.nothing_to_export</source>
        <translation >Rien à exporter. Merci de cocher au moins une case dans les paramètres d'exportation présent dans le second onglet </translation>
    </message>


    <!-- ******************* Network.py error message******************** -->


    <message>
        <source>q3m.error.processing</source>
        <translation >Il y a un problème avec le processing : vérifier s'il est activé sur votre plateforme (->Console python: import processing)</translation>
    </message>

    <message>
        <source>q3m.error.empty_attribute_name</source>
        <translation >Aucun nom n'a été donné pour la création d'une nouvelle colonne d'attribut dans la couche en mémoire</translation>
    </message>

    <message>
        <source>q3m.error.no_path_registered</source>
        <translation >Impossible de selectionner la route emprunté par l'utilisateur: celle ci n'a pas été créé</translation>
    </message>

    <message>
        <source>q3m.error.no_selection</source>
        <translation >Aucune route selectionné</translation>
    </message>


    <!-- ******************* Path.py error message******************** -->


    <message>
        <source>q3m.error.buffer_range</source>
        <translation >La taille du tampon renseigné est trop petite</translation>
    </message>

    <message>
        <source>q3m.error.wrong_speed_column</source>
        <translation >Impossible de trouver la colonne d'attribut renseigné dans la couche de point </translation>
    </message>

    <message>
        <source>q3m.error.negative_speed_limit</source>
        <translation >La limite de vitesse renseigné dans les paramètres ne peut être inférieur à 0</translation>
    </message>

    <message>
        <source>q3m.error.snap_points_along_line</source>
        <translation >Une erreur est survenue lors du matching par vitesse</translation>
    </message>

    <message>
        <source>q3m.error.empty_layer</source>
        <translation >La couche utilisé pour cet algorithme est vide</translation>
    </message>

    <message>
        <source>q3m.error.point_out_of_range</source>
        <translation >Une partie des points se retrouvent matché à une distance plus grande que celle renseignée dans les paramètres. Nombre de points : </translation>
    </message>


    <!-- ******************* Matcheur.py error message******************** -->


    <message>
        <source>q3m.error.error_searching_radius</source>
        <translation >Le rayon de recherche renseigné dans l'onglet paramètre est trop petit</translation>
    </message>

    <message>
        <source>q3m.error.error_sigma</source>
        <translation >Le sigma renseigné dans l'onglet paramètre est trop petit</translation>
    </message>

    <message>
        <source>q3m.error.error_build_graph</source>
        <translation >Il y a une erreur dans la fonction build_graph</translation>
    </message>

    <message>
        <source>q3m.error.distance_matcher</source>
        <translation >Une erreur est survenue à cause de la librairie Leuvenmapmatching</translation>
    </message>


    <!-- ******************* LayerTraductor.py error message******************** -->
    
    
    <message>
        <source>q3m.error.not_a_layer</source>
        <translation >Le paramètre renseigné n'est pas de type QgsVectorLayer et ne peut donc pas être convertit</translation>
    </message>
    
    <message>
        <source>q3m.error.not_a_list</source>
        <translation >Le paramètre renseigné n'est pas une liste</translation>
    </message>

    <message>
        <source>q3m.error.conversion_error</source>
        <translation >Erreur lors de de la conversion des géometries. Le problème vient de l'encodage des données</translation>
    </message>

    <message>
        <source>q3m.error.wrong_oid_column</source>
        <translation >La valeur de la colonne OID est introuvable dans la couche de route </translation>
    </message>


    <!-- ******************* Geometry.py error message******************** -->


    <message>
        <source>q3m.error.invalid_input</source>
        <translation >Un paramètre de la fonction est vide ou possède une valeur compromettante</translation>
    </message>

    <message>
        <source>q3m.error.no_candidate_found</source>
        <translation >Aucune entité trouvé dans le rayon renseigné autour d'un des points</translation>
    </message>

    <message>
        <source>q3m.error.empty_list</source>
        <translation >Un des paramètres de la fonction à produit une erreur: Une liste vide à été détécté </translation>
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
