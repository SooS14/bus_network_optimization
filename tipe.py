# Transport scolaire en Côte d'or#

#On se focalise sur les alentours de Semur en Auxois.
#Le puits est Semur en Auxois, les sources les villages les plus éloignés du réseau. 
#Pour optimiser le réseau on se base avant tout sur le calcul des chemins
#de moindre distance tout en ayant, au final un réseau cohérent avec les
#attentes des usagers. Enfin on cherche à connaître les flux maximaux sur le réseau


from collections import OrderedDict
import copy


# Pour le moindre distance, on utilise les algorithmes de Floyd puis Dijstra

#On donne la matrice d'adjacence et le programme renvoie la matrice des distances
#minimales entre 2 sommets (3000 symbolise l'infini)
def Floyd(graph):
    n = len(graph)
    for i in range(0,n):
        for j in range(0,n):
            if (graph[i][j] == 0):
                graph[i][j] = 30000 
    for k in range(0,n):
        for i in range(0,n):
            for j in range(0,n):
                if graph[i][j] > graph[i][k] + graph[k][j]:
                    graph[i][j] = graph[i][k] + graph[k][j]
    return(graph)


def dijkstra(graph,depart,arrivee):
    #Initialisation :
    predecesseur = {}
    non_vus = graph.copy()
    chemin = []
    inf = 1000
    dist_min = {}
    #Chaque noeud est à une distance infinie du départ
    for sommet in graph :
        dist_min[sommet] = inf
    #Sauf le noeud de départ qui est à une distance nulle de lui même
    dist_min[depart] = 0

    while non_vus:
    #Tant que non_vus n'est pas vide :
        
        #Initialisation, on trouve le sommet le plus proche possible
        min_sommet = None
        for sommet in non_vus:
            if min_sommet is None :
                min_sommet = sommet
            elif dist_min[sommet] < dist_min[min_sommet]:
                min_sommet = sommet

        for fils, poids in graph[min_sommet].items():
        #Pour chaque voisin du sommet le plus proche :
            if poids + dist_min[min_sommet] < dist_min[fils] :
                #Permet d'actualiser le tableau dist_min avec la plus courte distance
                dist_min[fils] = poids + dist_min[min_sommet]
                predecesseur[fils] = min_sommet
                
        #Ne pas oublier d'enlever le sommet qui vient d'être traité
        non_vus.pop(min_sommet)

    #Ici, on reconstruit le plus court chemin en procédant à reculons, on s'arrête quand
    #on est revenu au départ
    actuel = arrivee
    while actuel != depart :
        #On ajoute les sommets au fur et à mesure jusqu'à ce que actuel = départ ou
        #jusqu'à ce que le chemin s'arrête.
        try:
            chemin.insert(0,actuel)
            actuel = predecesseur[actuel]
        except KeyError:
            print('pas de chemin')
            break
        
    if dist_min[arrivee] != inf:
        chemin = [depart] + chemin
        return(dist_min[arrivee],chemin)



#On privilégie l'algorithme de Dijkstra pour une question de complexité
#L'algorithme de Floyd fonctionne en s^3 alors que celui de Dijkstra en
#s^2 + a, avec s le nombre de sommets et a le nombre d'arcs.


#Pour modéliser notre réseau on adopte une implémentation des graphes en liste d'adjacence
#Pour cela on utilise des dictionnaires qui permettent un accès rapide au poids des arcs
#en utilisant le nom des villages.
#Le graph est découpé en 4 et représente les alentours de Semur-en-Auxois. Le poids des arrêtes
#est calculé en utilisant google maps et celles ci sont créées de manières à faire apparaître
#des chemins différents mais cohérents avec les routes de la région Les villages considérés
#sont ceux desservis par les bus du conseil régional.


semur_nord_est = {
    'montbard':{'crepand':3,'fain-les-montbards':6},
    'crepand':{'montigny-monfort':5,'montbard':3},
    'montigny-monfort':{'crepand':5,'seigny':11,'champ-oiseau':2.5},
    'champ-oiseau':{'montigny-monfort':2.5,'semur':8,'lantilly':3},
    'fresnes':{'fain-les-montbards':3},
    'fain-les-montbards':{'fresnes':3,'montbard':6,'seigny':5},
    'seigny':{'fain-les-montbards':5,'montigny-monfort':11,'les-granges':4},
    'les-granges':{'seigny':4,'grignon':1},
    'grignon':{'les-granges':1,'lantilly':4,'venarey':5.5,'gresigny':11.2},
    'lantilly':{'grignon':4,'champ-oiseau':3,'villars':5,'venarey':6.3},
    'villars':{'lantilly':5,'semur':6,'villenotte':2.5},
    'villenotte':{'semur':4,'massigny':2.5,'villars':2.5},
    'massigny':{'villenotte':2.5,'venarey':6},
    'venarey':{'massigny':6,'lantilly':6.3,'grignon':5.5,'gresigny':5,'darcey':10,'gissey':13,'alisse':4,'pouillenay':3.2,'mussy':3.3},
    'gresigny':{'venarey':5,'ampilly':15},
    'ampilly':{'gresigny':15},
    'darcey':{'venarey':10,'frolois':7},
    'frolois':{'darcey':7,'laperriere':7},
    'laperriere':{'frolois':7},
    'gissey':{'venarey':13,'verrey':10},
    'verrey':{'gissey':10},
    'alisse':{'venarey':4,'flavigny':6},
    'flavigny':{'alisse':6,'pouillenay':10},
    'pouillenay':{'mussy':5,'venarey':3.2,'flavigny':10,'semur':10.9},
    'mussy':{'pouillenay':5,'venarey':3.3},
    'semur':{'pouillenay':10.9,'villenotte':4,'villars':6,'champ-oiseau':8}}



semur_nord_ouest = {
    'st-remy':{'quincerot':5.4},
    'quincerot':{'st-remy':5.4,'quincy':1.3},
    'quincy':{'st-just':6.9,'st-germain-senailly':3.5,'quincerot':1.3},
    'st-germain-senailly':{'quincy':3.5,'moutiers-st-jean':7.9,'senailly':1.6},
    'senailly':{'st-germain-senailly':1.6,'viserny':3.8,'athie':3.3},
    'st-just':{'fain-moutiers':1.9,'quincy':6.9},
    'fain-moutiers':{'st-just':1.9,'moutiers-st-jean':3.1,'turley':5},
    'moutiers-st-jean':{'fain-moutiers':3.1,'st-germain-senailly':7.9,'athie':3.2},
    'athie':{'moutiers-st-jean':3.2,'tivauche':4.6,'viserny':2.6,'senailly':3.3},
    'viserny':{'athie':2.6,'senailly':3.8,'villaines-prevotes':4,'jeux-bard':4.4,'genay':5},
    'villaines-prevotes':{'viserny':4,'charentois':5.5},
    'turley':{'fain-moutiers':5,'corsaint':3.1,'epoissote':6.3},
    'corsaint':{'turley':3.1,'tivauche':2.9,'monceau':3},
    'tivauche':{'athie':4.6,'corsaint':2.9,'bard-epoisses':2.4},
    'bard-epoisses':{'tivauche':2.4,'corrombles':4.5,'jeux-bard':3.8},
    'jeux-bard':{'bard-epoisses':3.8,'viserny':4.4,'genay':4.2,},
    'genay':{'jeux-bard':4.2,'millery':2.8,'chevigny':3.7,'viserny':5},
    'chevigny':{'charentois':3.3,'genay':3.7},
    'charentois':{'chevigny':3.3,'villaines-prevotes':5.5,'semur':3},
    'epoissote':{'turley':6.3,'epoisses':1.3,'monceau':1.1},
    'monceau':{'epoissote':1.1,'corsaint':3,'epoisses':1.9,'corrombles':1},
    'corrombles':{'epoisses':2.4,'monceau':1,'bard-epoisses':4.5,'torcy':5.1},
    'torcy':{'corrombles':5.1,'millery':8.3},
    'millery':{'torcy':8.3,'semur':5,'genay':2.8},
    'toutry':{'epoisses':4.7,'vieux-chateau':4.5},
    'vieux-chateau':{'toutry':4.5,'montberthault':2.8},
    'montberthault':{'vieux-chateau':2.8,'epoisses':4.7},
    'epoisses':{'toutry':4.7,'montberthault':4.7,'changy':1.5,'epoissote':1.3,'monceau':1.9,'corrombles':2.4},
    'changy':{'epoisses':1.5,'semur':15},
    'semur':{'changy':15,'millery':5,'charentois':3}}


semur_sud_est = {
    'semur':{'juilly':6,'massene':3.9,'pont-massene':3.9},
    'juilly':{'semur':6,'souhey':2.2,'massene':3.9},
    'souhey':{'juilly':2.2,'st-euphrone':3.8,'magny':1},
    'magny':{'souhey':1,'chassey':3},
    'chassey':{'magny':3,'marigny':3},
    'marigny':{'chassey':3,'leugny':6,'arnay-vitteaux':6},
    'leugny':{'marigny':6,'roche-vanneau':1},
    'roche-vanneau':{'leugny':1,'clirey':2,'arnay-vitteaux':6.1},
    'clirey':{'roche-vanneau':2},
    'arnay-vitteaux':{'marigny':6,'roche-vanneau':6.1,'posanges':5.3},
    'posanges':{'charigny':10.4,'arnay-vitteaux':5.3,'vitteaux':3.1},
    'charigny':{'posanges':10.4,'villeneuve-charigny':3.4,'montigny-armançon':5.3,'braux':3.6},
    'villeneuve-charigny':{'st-euphrone':6,'montigny-armançon':1.9,'charigny':3.4},
    'st-euphrone':{'massene':1.2,'villeneuve-charigny':6,'souhey':3.8},
    'massene':{'st-euphrone':1.2,'juilly':3.9,'pont-massene':2.1,'semur':3.9},
    'pont-massene':{'semur':3.9,'massene':2.1,'allerey':2.7},
    'allerey':{'pont-massene':2.7,'flee':2.2},
    'flee':{'montigny-armançon':4.1,'allerey':2.2,'roilly':2.1},
    'montigny-armançon':{'flee':4.1,'brianny':2.8,'villeneuve-charigny':1.9,'charigny':5.3},
    'roilly':{'flee':2.1,'brianny':3.5,'thil':5.1},
    'brianny':{'roilly':3.5,'montigny-armançon':2.8,'braux':4.8,'marcigny':3.1},
    'braux':{'charigny':3.6,'brianny':4.8,'pont-royal':3.1},
    'thil':{'roilly':5.1,'nan-sous-thil':1.9},
    'nan-sous-thil':{'thil':1.9,'clamerey':6.9,'pluvier':3.5},
    'clamerey':{'nan-sous-thil':6.9,'marcigny':3.9,'pont-royal':1.7,'normier':2.7},
    'marcigny':{'brianny':3.1,'clamerey':3.9},
    'pont-royal':{'braux':3.1,'clamerey':1.7,'st-thibault':4.8},
    'st-thibault':{'pont-royal':4.8,'vitteaux':6.5,'normier':4.6,'gissey-vieil':6.6},
    'vitteaux':{'posanges':3.1,'saffres':5.1,'st-thibault':6.5},
    'saffres':{'vitteaux':5.1,'gissey-vieil':14.7,'pouilly-auxois':16.4},
    'pouilly-auxois':{'saffres':16.4,'gissey-vieil':9.8},
    'gissey-vieil':{'saffres':14.7,'st-thibault':6.6,'pouilly-auxois':9.8,'noidan':7.4},
    'normier':{'st-thibault':4.6,'clamerey':2.7,'noidan':3.6},
    'noidan':{'normier':3.6,'gissey-vieil':7.4,'pluvier':2.5,'chazelle':3.9},
    'pluvier':{'nan-sous-thil':3.5,'noidan':2.5,'chazelle':2.8},
    'chazelle':{'motte-ternant':4.2,'fontagny':1.7,'pluvier':2.8,'noidan':3.9},
    'fontagny':{'chazelle':1.7,'chausseroze':3.5},
    'chausseroze':{'fontagny':3.5,'motte-ternant':3.5},
    'motte-ternant':{'chausseroze':3.5,'chazelle':4.2}}


semur_sud_ouest = {
    'semur':{'cernois':6.5,'courcelles-semur':6.3,'bierre-semur': 11.6},
    'cernois':{'semur':6.5,'chassenay':2.5},
    'courcelles-semur':{'semur':6.3,'chassenay':3.9,'ruffey':2.3},
    'chassenay':{'torcy':7.1,'bourbilly':3.1,'courcelles-semur':3.9,'cernois':2.5},
    'torcy':{'chassenay':7.1,'foux':1.4},
    'foux':{'forleans':1,'torcy':1.4},
    'forleans':{'fremoy':5.9,'foux':1,'bourbilly':6.7},
    'bourbilly':{'forleans':6.7,'chassenay':3.1,'ruffey':10.6,'courcelles-fremoy':6.9},
    'ruffey':{'bourbilly':10.6,'beauregard':4.4,'courcelles-semur':2.3,'bierre-semur':4.1},
    'beauregard':{'grenouilly':4.2,'ruffey':4.4,'courcelles-fremoy':11.3},
    'bierre-semur':{'ruffey':4.1,'lucenay':1.4,'semur':11.4},
    'lucenay':{'bierre-semur':1.4,'montigny-barthelemy':3.1,'aisy-thil':3.4},
    'grenouilly':{'montigny-barthelemy':3.7,'beauregard':4.2,'dompiere':2.4,'chamont':4.4},
    'courcelles-fremoy':{'beauregard':11.3,'bourbilly':6.9,'fremoy':2},
    'fremoy':{'charmee':2.9,'courcelles-fremoy':2,'forleans':5.9},
    'charmee':{'fremoy':2.9,'sincey-rouvray':2.7},
    'sincey-rouvray':{'charmee':2.7,'rouvray':2.6},
    'rouvray':{'vernon':4.5,'st-andeux':3.5,'sincey-rouvray':2.6},
    'vernon':{'rouvray':4.5,'bierre-morvan':2.4,'chamont':3.3},
    'chamont':{'potenay':2.9,'vernon':3.3,'grenouilly':4.4},
    'st-andeux':{'rouvray':3.5,'st-germain':3.9},
    'st-germain':{'st-andeux':3.9,'roche-brenil':4.6},
    'bierre-morvan':{'vernon':2.4,'roche-brenil':3.6},
    'roche-brenil':{'bierre-morvan':3.6,'potenay':4.1,'molphey':5.8},
    'potenay':{'chamont':2.9,'roche-brenil':4.1,'dompiere':3.2},
    'dompiere':{'potenay':3.2,'grenouilly':2.4,'aisy-thil':5.5},
    'aisy-thil':{'montigny-barthelemy':4.1,'lucenay':3.4,'dompiere':5.5,'juillenay':5.8,'vic-thil':4.4},
    'montigny-barthelemy':{'grenouilly':3.7,'aisy-thil':4.1,'lucenay':3.1},
    'vic-thil':{'aisy-thil':4.4,'juillenay':3.4},
    'juillenay':{'aisy-thil':5.8,'arcenay':3.2,'vic-thil':3.4,'montlay-auxois':1.2},
    'arcenay':{'juillenay':3.2,'molphey':5.5},
    'molphey':{'roche-brenil':5.8,'st-didier':3.4,'arcenay':5.5},
    'st-didier':{'molphey':3.4,'chanteau':2.2},
    'chanteau':{'saulieu':4.9,'st-didier':2.2},
    'saulieu':{'chanteau':4.9,'montlay-auxois':10.6},
    'montlay-auxois':{'saulieu':10.6,'juillenay':1.2}}


#Les graphes dénommés semur_localisation_poids prennent en compte le nombre d'élèves présents dans
#un village (représenté par la clef graph[sommet][poids])


semur_nord_est_poids = {
    'montbard':{'poids':164,'crepand':3,'fain-les-montbards':6},
    'crepand':{'poids':28,'montigny-monfort':5,'montbard':3},
    'montigny-monfort':{'poids':16,'crepand':5,'seigny':11,'champ-oiseau':2.5},
    'champ-oiseau':{'poids':7,'montigny-monfort':2.5,'semur':8,'lantilly':3},
    'fresnes':{'poids':5,'fain-les-montbards':3},
    'fain-les-montbards':{'poids':6,'fresnes':3,'montbard':6,'seigny':5},
    'seigny':{'poids':5,'fain-les-montbards':5,'montigny-monfort':11,'les-granges':4},
    'les-granges':{'poids':0,'seigny':4,'grignon':1},
    'grignon':{'poids':6,'les-granges':1,'lantilly':4,'venarey':5.5,'gresigny':11.2},
    'lantilly':{'poids':19,'grignon':4,'champ-oiseau':3,'villars':5,'venarey':6.3},
    'villars':{'poids':13,'lantilly':5,'semur':6,'villenotte':2.5},
    'villenotte':{'poids':0,'semur':4,'massigny':2.5,'villars':2.5},
    'massigny':{'poids':30,'villenotte':2.5,'venarey':6},
    'venarey':{'poids':70,'mussy':3.3,'massigny':6,'lantilly':6.3,'grignon':5.5,'gresigny':5,'darcey':10,'gissey':13,'alisse':4,'pouillenay':3.2},
    'gresigny':{'poids':3,'venarey':5,'ampilly':15,'grignon':11.2},
    'ampilly':{'poids':1,'gresigny':15},
    'darcey':{'poids':2,'venarey':10,'frolois':7},
    'frolois':{'poids':2,'darcey':7,'laperriere':7},
    'laperriere':{'poids':1,'frolois':7},
    'gissey':{'poids':2,'venarey':13,'verrey':10},
    'verrey':{'poids':1,'gissey':10},
    'alisse':{'poids':2,'venarey':4,'flavigny':6},
    'flavigny':{'poids':1,'alisse':6,'pouillenay':10},
    'pouillenay':{'poids':12,'mussy':5,'venarey':3.2,'flavigny':10},
    'mussy':{'poids':0,'pouillenay':5,'venarey':3.3},
    'semur':{'poids':0,'villenotte':4,'villars':6,'champ-oiseau':8}}


semur_nord_ouest_poids = {
    'st-remy':{'poids':9,'montbard':4.7,'quincerot':5.4},
    'quincerot':{'poids':4,'st-remy':5.4,'quincy':1.3},
    'quincy':{'poids':6,'st-just':6.9,'st-germain-senailly':3.5,'quincerot':1.3},
    'st-germain-senailly':{'poids':3,'quincy':3.5,'moutiers-st-jean':7.9,'senailly':1.6},
    'senailly':{'poids':3,'st-germain-senailly':1.6,'viserny':3.8,'athie':3.3},
    'st-just':{'poids':0,'fain-moutiers':1.9,'quincy':6.9},
    'fain-moutiers':{'poids':1,'st-just':1.9,'moutiers-st-jean':3.1,'turley':5},
    'moutiers-st-jean':{'poids':19,'fain-moutiers':3.1,'st-germain-senailly':7.9,'athie':3.2},
    'athie':{'poids':4,'moutiers-st-jean':3.2,'tivauche':4.6,'viserny':2.6,'senailly':3.3},
    'viserny':{'poids':12,'athie':2.6,'senailly':3.8,'villaines-prevotes':4,'jeux-bard':4.4,'genay':5},
    'villaines-prevotes':{'poids':11,'charentois':5.5,'viserny':4},
    'turley':{'poids':0,'fain-moutiers':5,'corsaint':3.1,'epoissote':6.3},
    'corsaint':{'poids':10,'turley':3.1,'tivauche':2.9,'monceau':3},
    'tivauche':{'poids':0,'athie':4.6,'corsaint':2.9,'bard-epoisses':2.4},
    'bard-epoisses':{'poids':0,'tivauche':2.4,'corrombles':4.5,'jeux-bard':3.8},
    'jeux-bard':{'poids':11,'bard-epoisses':3.8,'viserny':4.4,'genay':4.2,},
    'genay':{'poids':23,'jeux-bard':4.2,'millery':2.8,'chevigny':3.7,'viserny':5},
    'chevigny':{'poids':0,'charentois':3.3,'genay':3.7},
    'charentois':{'poids':0,'chevigny':3.3,'villaines-prevotes':5.5,'semur':3},
    'epoissote':{'poids':0,'turley':6.3,'epoisses':1.3,'monceau':1.1},
    'monceau':{'poids':0,'epoissote':1.1,'corsaint':3,'epoisses':1.9,'corrombles':1},
    'corrombles':{'poids':17,'epoisses':2.4,'monceau':1,'bard-epoisses':4.5,'torcy':5.1},
    'torcy':{'poids':11,'corrombles':5.1,'millery':8.3},
    'millery':{'poids':21,'torcy':8.3,'semur':5,'genay':2.8},
    'toutry':{'poids':24,'epoisses':4.7,'vieux-chateau':4.5},
    'vieux-chateau':{'poids':3,'toutry':4.5,'montberthault':2.8},
    'montberthault':{'poids':13,'vieux-chateau':2.8,'epoisses':4.7},
    'epoisses':{'poids':54,'toutry':4.7,'montberthault':4.7,'changy':1.5,'epoissote':1.3,'monceau':1.9,'corrombles':2.4},
    'changy':{'poids':0,'epoisses':1.5,'semur':15},
    'semur':{'poids':0,'changy':15,'millery':5,'charentois':3}}


semur_sud_est_poids = {
    'semur':{'poids':0,'juilly':6,'massene':3.9,'pont-massene':3.9},
    'juilly':{'poids':2,'semur':6,'souhey':2.2,'massene':3.9},
    'souhey':{'poids':4,'juilly':2.2,'st-euphrone':3.8,'magny':1},
    'magny':{'poids':3,'souhey':1,'chassey':3},
    'chassey':{'poids':5,'magny':3,'marigny':3},
    'marigny':{'poids':4,'chassey':3,'leugny':6,'arnay-vitteaux':6},
    'leugny':{'poids':0,'marigny':6,'roche-vanneau':1},
    'roche-vanneau':{'poids':0,'leugny':1,'clirey':2,'arnay-vitteaux':6.1},
    'clirey':{'poids':0,'roche-vanneau':2},
    'arnay-vitteaux':{'poids':0,'marigny':6,'roche-vanneau':6.1,'posanges':5.3},
    'posanges':{'poids':0,'charigny':10.4,'arnay-vitteaux':5.3,'vitteaux':3.1},
    'charigny':{'poids':4,'posanges':10.4,'villeneuve-charigny':3.4,'montigny-armançon':5.3,'braux':3.6},
    'villeneuve-charigny':{'poids':5,'st-euphrone':6,'montigny-armançon':1.9,'charigny':3.4},
    'st-euphrone':{'poids':17,'massene':1.2,'villeneuve-charigny':6,'souhey':3.8},
    'massene':{'poids':0,'st-euphrone':1.2,'juilly':3.9,'pont-massene':2.1,'massene':3.9},
    'pont-massene':{'poids':16,'semur':3.9,'massene':2.1,'allerey':2.7},
    'allerey':{'poids':0,'pont-massene':2.7,'flee':2.2},
    'flee':{'poids':11,'montigny-armançon':4.1,'allerey':2.2,'roilly':2.1},
    'montigny-armançon':{'poids':12,'flee':4.1,'brianny':2.8,'villeneuve-charigny':1.9,'charigny':5.3},
    'roilly':{'poids':4,'flee':2.1,'brianny':3.5,'thil':5.1},
    'brianny':{'poids':10,'roilly':3.5,'montigny-armançon':2.8,'braux':4.8,'marcigny':3.1},
    'braux':{'poids':4,'charigny':3.6,'brianny':4.8,'pont-royal':3.1},
    'thil':{'poids':0,'roilly':5.1,'nan-sous-thil':1.9},
    'nan-sous-thil':{'poids':14,'thil':1.9,'clamerey':6.9,'pluvier':3.5},
    'clamerey':{'poids':6,'nan-sous-thil':6.9,'marcigny':3.9,'pont-royal':1.7,'normier':2.7},
    'marcigny':{'poids':3,'brianny':3.1,'clamerey':3.9},
    'pont-royal':{'poids':0,'braux':3.1,'clamerey':1.7,'st-thibault':4.8},
    'st-thibault':{'poids':0,'pont-royal':4.8,'vitteaux':6.5,'normier':4.6,'gissey-vieil':6.6},
    'vitteaux':{'poids':8,'posanges':3.1,'saffres':5.1,'st-thibault':6.5},
    'saffres':{'poids':0,'vitteaux':5.1,'gissey-vieil':14.7,'pouilly-auxois':16.4},
    'pouilly-auxois':{'poids':0,'saffres':16.4,'gissey-vieil':9.8},
    'gissey-vieil':{'poids':0,'saffres':14.7,'st-thibault':6.6,'pouilly-auxois':9.8,'noidan':7.4},
    'normier':{'poids':0,'st-thibault':4.6,'clamerey':2.7,'noidan':3.6},
    'noidan':{'poids':1,'normier':3.6,'gissey-vieil':7.4,'pluvier':2.5,'chazelle':3.9},
    'pluvier':{'poids':0,'nan-sous-thil':3.5,'noidan':2.5,'chazelle':2.8},
    'chazelle':{'poids':0,'motte-ternant':4.2,'fontagny':1.7,'pluvier':2.8,'noidan':3.9},
    'fontagny':{'poids':12,'chazelle':1.7,'chausseroze':3.5},
    'chausseroze':{'poids':15,'fontagny':3.5,'motte-ternant':3.5},
    'motte-ternant':{'poids':0,'chausseroze':3.5,'chazelle':4.2}}


semur_sud_ouest_poids = {
    'semur':{'poids':0,'cernois':6.5,'courcelles-semur':6.3,'bierre-semur':11.6},
    'cernois':{'poids':0,'semur':6.5,'chassenay':2.5},
    'courcelles-semur':{'poids':20,'semur':6.3,'chassenay':3.9,'ruffey':2.3},
    'chassenay':{'poids':18,'torcy':7.1,'bourbilly':3.1,'courcelles-semur':3.9,'cernois':2.5},
    'torcy':{'poids':0,'chassenay':7.1,'foux':1.4},
    'foux':{'poids':0,'forleans':1,'torcy':1.4},
    'forleans':{'poids':9,'fremoy':5.9,'foux':1,'bourbilly':6.7},
    'bourbilly':{'poids':0,'forleans':6.7,'chassenay':3.1,'ruffey':10.6,'courcelles-fremoy':6.9},
    'ruffey':{'poids':0,'bourbilly':10.6,'beauregard':4.4,'courcelles-semur':2.3,'bierre-semur':4.1},
    'beauregard':{'poids':7,'grenouilly':4.2,'ruffey':4.4,'courcelles-fremoy':11.3},
    'bierre-semur':{'poids':4,'ruffey':4.1,'roilly':3.7,'lucenay':1.4,'semur':11.6},
    'lucenay':{'poids':6,'bierre-semur':1.4,'montigny-barthelemy':3.1,'aisy-thil':3.4},
    'grenouilly':{'poids':0,'montigny-barthelemy':3.7,'beauregard':4.2,'dompiere':2.4,'chamont':4.4},
    'courcelles-fremoy':{'poids':20,'beauregard':11.3,'bourbilly':6.9,'fremoy':2},
    'fremoy':{'poids':8,'charmee':2.9,'courcelles-fremoy':2,'forleans':5.9},
    'charmee':{'poids':0,'fremoy':2.9,'sincey-rouvray':2.7},
    'sincey-rouvray':{'poids':1,'charmee':2.7,'rouvray':2.6},
    'rouvray':{'poids':10,'vernon':4.5,'st-andeux':3.5,'sincey-rouvray':2.6},
    'vernon':{'poids':0,'rouvray':4.5,'bierre-morvan':2.4,'chamont':3.3},
    'chamont':{'poids':0,'potenay':2.9,'vernon':3.3,'grenouilly':4.4},
    'st-andeux':{'poids':2,'rouvray':3.5,'st-germain':3.9},
    'st-germain':{'poids':4,'st-andeux':3.9,'roche-brenil':4.6},
    'bierre-morvan':{'poids':0,'vernon':2.4,'roche-brenil':3.6},
    'roche-brenil':{'poids':13,'bierre-morvan':3.6,'potenay':4.1,'molphey':5.8},
    'potenay':{'poids':0,'chamont':2.9,'roche-brenil':4.1,'dompiere':3.2},
    'dompiere':{'poids':21,'potenay':3.2,'grenouilly':2.4,'aisy-thil':5.5},
    'aisy-thil':{'poids':19,'montigny-barthelemy':4.1,'lucenay':3.4,'dompiere':5.5,'juillenay':5.8,'vic-thil':4.4},
    'montigny-barthelemy':{'poids':5,'grenouilly':3.7,'aisy-thil':4.1,'lucenay':3.1},
    'vic-thil':{'poids':15,'aisy-thil':4.4,'juillenay':3.4},
    'juillenay':{'poids':1,'aisy-thil':5.8,'arcenay':3.2,'vic-thil':3.4,'montlay-auxois':1.2},
    'arcenay':{'poids':8,'juillenay':3.2,'molphey':5.5},
    'molphey':{'poids':2,'roche-brenil':5.8,'st-didier':3.4,'arcenay':5.5},
    'st-didier':{'poids':0,'molphey':3.4,'chanteau':2.2},
    'chanteau':{'poids':5,'saulieu':4.9,'st-didier':2.2},
    'saulieu':{'poids':442,'chanteau':4.9,'montlay-auxois':10.6},
    'montlay-auxois':{'poids':4,'saulieu':10.6,'juillenay':1.2}}



#Il serait interessant de connaître le nombre de bus optimal pour transporter les élèves.
#On va d'abord créer des lignes à partir de la connaissance des sources du graph
#puis, pour chaque ligne on cherche le nombre de bus necessaires pour le transport
#des élèves qui l'empreintent à des heures bien définies(pour le secondaire le
#ramassage est effectué entre 8-9h et 18-19h.
#Il s'agit de passer par les plus courts chemins mais de aussi de "vider" le graphe


#Premier traitement du graphe :
#Il faut :

#_En utilisant l'algorithme de dijkstra trouver les lignes de bus les plus courtes
#sachant les sources

def creation_lignes(graph,l_sources,puit):
    lignes = []
    for i in l_sources:
        ligne = dijkstra(graph,i,puit)
        lignes.append(ligne)
    return(lignes)

#_Calculer le nombre de bus sur la première ligne puis enlever le poids des élèves de cette ligne
#_Iterer sur la liste des lignes
def nombre_bus_tot(graph_poids,list_ligne):
    copy_graph = copy.deepcopy(graph_poids)
    bus = []
    for j in list_ligne :
    #Pour chaque ligne :
        t = 0
        longueur,ligne = j
        for i in ligne:
        #Pour chaque sommet de la ligne on récupère le nombre d'élève
            nb_eleves = copy_graph[i]['poids']
            copy_graph[i]['poids'] = 0
            t = t + nb_eleves
        #On considère que les bus ont 50 places
        if t%50 != 0:
            bus.append((t//50+1,t%50,longueur,ligne))
        else:
            bus.append((t/50,t%50,longueur,ligne))
    #On renvoie le nombre de bus, le remplissage du dernier bus et le graph (pour savoir si il
    #a été correctement "vidé"
    return(bus,copy_graph)

def total_eleves_graph(graph):
    total_eleves = 0
    for i in graph.keys():
        total_eleves = total_eleves + graph[i]['poids']
    return(total_eleves)

#_Faire tourner un test qui renvoie combien il reste d'élèves et où ils sont localisés
def test_eleves_restant(graph):
    eleves_restant = []
    t = 0
    for i in graph.keys() :
        if graph[i]['poids'] != 0 :
            t = graph[i]['poids'] + t
            eleves_restant.append((i,graph[i]['poids']))
    return(eleves_restant,t)


def affiche_res(graph_poids,l_ligne) :
    bus,nouveau_graph_poids = nombre_bus_tot(graph_poids,l_ligne)
    eleves_restant,t = test_eleves_restant(nouveau_graph_poids)
    total_eleves = total_eleves_graph(semur_nord_est_poids)

    print("### nombre bus, eleves dernier bus, longueur ligne, ligne \n")
    for ligne_bus in bus :
        print("# ",ligne_bus)
        
    print("eleves_restant :", eleves_restant, "; il reste :", t, "eleves sur", total_eleves, "au total")
    print(" ")
    print(" ")    


print("\n\n###########Premier Traitement###########\n")

#test semur_nord_est
l_ligne = creation_lignes(semur_nord_est,['montbard','fresnes','ampilly','laperriere','verrey','pouillenay'],'semur')
affiche_res(semur_nord_est_poids,l_ligne)


#test semur_nord_ouest
l_ligne = creation_lignes(semur_nord_ouest,['st-remy','st-just','tivauche','bard-epoisses','toutry','vieux-chateau'],'semur')
affiche_res(semur_nord_ouest_poids,l_ligne)


#test semur_sud_ouest
l_ligne = creation_lignes(semur_sud_ouest,['forleans','st-germain','chanteau','saulieu','arcenay','vic-thil'],'semur')
affiche_res(semur_sud_ouest_poids,l_ligne)


#test semur_sud_est
l_ligne = creation_lignes(semur_sud_est,['arnay-vitteaux','posanges','pouilly-auxois','noidan','motte-ternant'],'semur')
affiche_res(semur_sud_est_poids, l_ligne)



#A l'issue de ce premier traitement on obtient des lignes optimales en terme de distance
#mais inefficacent en ce qui concerne le ramassage des usagers. Certaines lignes sont inutiles
#alors que des villages ne sont pas desservis.



#Second traitement :

#On peut utiliser dijkstra sur une liste de sommets oubliés pour créer de nouvelles lignes
#reliant les villages oubliés de manière optimale en terme de distance.

def ligne_secondaire(graph,liste_oublie,arrivee):
    l = liste_oublie + [arrivee]
    l_prime = []
    distance = 0
    n = len(l)
    for i in range(0,n-1):
        pere = l[i]
        fils = l[i+1]
        #on calcul le plus court chemin entre chaque élément de la liste
        dist,chemin = dijkstra(graph,pere,fils)
        m = len(chemin)              #sert à supprimer les doublons dans chemin
        del chemin[m-1]              #
        #à chaque boucle on concatène les chemins trouvés et on additionne la distance
        distance += dist
        l_prime = l_prime + chemin   
    return(distance,l_prime + [arrivee])


#L'algorithme n'est pas très autonome, on doit remplir liste_oublie du sommet
#le plus éloigné au sommet le pus proche de l'arrivée.
#Néanmoins il permet de renvoyer des chemins cohérents et optimaux.
#On peut de plus raccorder ces chemins à une source proche et supprimer les
#lignes inutiles. 

#Semur nord est :
#On supprime la ligne de source 'fresnes' et on l'utilise pour:
a = ligne_secondaire(semur_nord_est,
                      ['fresnes','seigny','grignon','lantilly','villars'],
                      'semur')

#Semur nord est :
#on supprime la ligne de source 'tivauche' et on l'utilise pour:
b = ligne_secondaire(semur_nord_ouest,
                      ['tivauche','corsaint','corrombles','torcy'],
                      'semur')


#Semur sud ouest :
#On créer une nouvelle ligne de source 'st-Andeux'
c1 = ligne_secondaire(semur_sud_ouest,
                     ['st-andeux','rouvray','sincey-rouvray','fremoy','courcelles-fremoy'],
                     'semur')
#On modifie la ligne de source 'saulieu'
c2 = ligne_secondaire(semur_sud_ouest,
                     ['saulieu','vic-thil'],
                     'semur')
#On supprime les lignes de sources 'Vic-Thil' et 'Arcenay'


#Semur sud est :
#On modifie la ligne de source 'Motte-Ternant':
d1 = ligne_secondaire(semur_sud_est,
                      ['motte-ternant','chausseroze','fontagny'],
                      'semur')
#On supprime la ligne de source 'Noidan' et on l'utilise pour:
d2 = ligne_secondaire(semur_sud_est,
                      ['noidan','clamerey','marcigny','brianny','montigny-armançon'],
                      'semur')
#On modifie la ligne de source 'Pouilly-Auxois':
d3 = ligne_secondaire(semur_sud_est,
                      ['posanges','vitteaux','braux','charigny','villeneuve-charigny','st-euphrone'],
                      'semur')



#On effectue une rétroaction en reprenant le procédé du premier traitement:
print("\n\n###########Second Traitement###########\n")

#Test semur nord est
l_ligne = [(18.5, ['montbard', 'crepand', 'montigny-monfort', 'champ-oiseau', 'semur']),
           a, #(28, ['fresnes', 'fain-les-montbards', 'seigny', 'les-granges', 'grignon', 'lantilly', 'villars', 'semur']),
           (32.5, ['ampilly', 'gresigny', 'venarey', 'massigny', 'villenotte', 'semur']),
           (36.5, ['laperriere', 'frolois', 'darcey', 'venarey', 'massigny', 'villenotte', 'semur']),
           (35.5, ['verrey', 'gissey', 'venarey', 'massigny', 'villenotte', 'semur']),
           (10.9, ['pouillenay', 'semur'])]
affiche_res(semur_nord_est_poids, l_ligne)


#Test semur nord ouest
l_ligne = [(28.1, ['st-remy', 'quincerot', 'quincy', 'st-germain-senailly', 'senailly', 'viserny', 'villaines-prevotes', 'charentois', 'semur']),
           (23.3, ['st-just', 'fain-moutiers', 'moutiers-st-jean', 'athie', 'viserny', 'villaines-prevotes', 'charentois', 'semur']),
           b,#(25.3, ['tivauche', 'corsaint', 'monceau', 'corrombles', 'torcy', 'millery', 'semur']),
           (15.8, ['bard-epoisses', 'jeux-bard', 'genay', 'millery', 'semur']),
           (21.2, ['toutry', 'epoisses', 'changy', 'semur']),
           (24.0, ['vieux-chateau', 'montberthault', 'epoisses', 'changy', 'semur'])]
affiche_res(semur_nord_ouest_poids, l_ligne)


#Test semur sud ouest
l_ligne = [(18.5, ['forleans', 'foux', 'torcy', 'chassenay', 'cernois', 'semur']),
           (31.5, ['st-germain', 'roche-brenil', 'potenay', 'dompiere', 'grenouilly', 'beauregard', 'ruffey', 'courcelles-semur', 'semur']),
           (36.3, ['chanteau', 'st-didier', 'molphey', 'arcenay', 'juillenay', 'aisy-thil', 'lucenay', 'bierre-semur', 'semur']),
           c2,#(35.8, ['saulieu', 'montlay-auxois', 'juillenay', 'vic-thil', 'aisy-thil', 'lucenay', 'bierre-semur', 'semur']),
           c1#(32.7, ['st-andeux', 'rouvray', 'sincey-rouvray', 'charmee', 'fremoy', 'courcelles-fremoy', 'bourbilly', 'chassenay', 'cernois', 'semur'])
           ]
affiche_res(semur_sud_ouest_poids, l_ligne)


#Test semur sud est
l_ligne = [(21.2, ['arnay-vitteaux', 'marigny', 'chassey', 'magny', 'souhey', 'juilly', 'semur']),
           d3,#(35.6, ['posanges', 'vitteaux', 'st-thibault', 'pont-royal', 'braux', 'charigny', 'villeneuve-charigny', 'st-euphrone', 'massene', 'semur']),
           d2,#(29.0, ['noidan', 'normier', 'clamerey', 'marcigny', 'brianny', 'montigny-armançon', 'flee', 'allerey', 'pont-massene', 'semur']),
           d1#(32.9, ['motte-ternant', 'chausseroze', 'fontagny', 'chazelle', 'pluvier', 'nan-sous-thil', 'thil', 'roilly', 'flee', 'allerey', 'pont-massene', 'semur'])
           ]
affiche_res(semur_sud_est_poids, l_ligne)


#À la suite de ce second traitement, les lignes sont bien plus cohérentes avec la disposition
#des usagers: on passe de 20% d'oubliés en pour tout le graphe à seulement 8 personnes sur 1500.
#De plus, les lignes recouvrent une plus grande partie du graph.

#Néanmoins il reste le problème du remplissage des bus. Certains bus ne transportent que quelques
#passagers. Il faut donc calculer le graphe des places disponibles sur chaque arrête pour pouvoir
#y appliquer l'algorithme de Ford-Fulkerson. On pourra alors réduire le nombre de places vides grâce
#à des bus plus petits (30 ou 20 places) ou connaître le nombre maximum d'usagers que l'on peut
#intégrer au réseau.


#Troisième traitement :

#Cet fonction permet créer un graph représentant le nombre de passagers transportés sur chaque arrête.
def cumul_des_usagers(graph,graph_poids,list_lignes):
    n = len(graph_poids)

    #On créé le nouveau graph : 
    graph_flux = copy.deepcopy(graph)
    for i in graph_flux.keys():
        for j in graph_flux.keys():
            graph_flux[i][j] = 0
            
    for ligne in list_lignes :
        t = 0
        n = len(ligne)
        for j in range(0,n-1):
            #pour chaque ligne on considère :
            pere = ligne[j]
            fils = ligne[j+1]
            #il s'agit des usagers qui montent dans le bus au fur et à mesure
            t = t + graph_poids[pere]['poids']
            #si le poids sur l'arc est moins intéressant, on le remplace
            if t > graph_flux[pere][fils]:
                graph_flux[pere][fils] = t
                graph_flux[fils][pere] = t

    #pour enlever les arcs inutiles (sans passagers)
    for i in graph_flux.keys():
        for j in graph_flux.keys():
            if graph_flux[i][j] == 0 :
                del graph_flux[i][j]

    return(graph_flux)


                       
#on connaît les bus sur chaque ligne et le flux des usagers du scolaire, on
#calcul le graphe des capacités (grâce aux résultats de cumul_des_usagers et nombre_bus_tot)
def places_libres(bus,graph_flux):
    graph_capa = copy.deepcopy(graph_flux)
    for quad in bus:
        nb_bus,remplissage,longueur,ligne = quad
        n = len(ligne)
        
        for i in range(0,n-1):
            pere = ligne[i]
            fils = ligne[i+1]
            #on retranche, sur chaque arc, au nombre d'élèves le nombre de places disponibles
            #prend en compte le cas où plusieurs lignes passent par le même arc
            graph_capa[pere][fils] = graph_capa[pere][fils] - (nb_bus * 50)
            graph_capa[fils][pere] = graph_capa[fils][pere] - (nb_bus * 50)

    #le nombre de place est excédentaire donc tous les coefficeints de graph_capa sont < 0
    for i in graph_capa.keys():
        for j in graph_capa[i].keys():
            graph_capa[i][j]  = (-1) * graph_capa[i][j]
            
    return(graph_capa)



#Enfin on calcul les flux maximaux grâce à l'algorithme de Ford-Fulkerson et ses auxiliaires :
#La fonction fordfulk utilise une représentation en matrice d'adjacence représentée par une liste
#de listes (plus facile à implémenter) on utilise ces 3 fonctions pour changer de mode de représentation.

def dico_to_list(dic):
    # on ordonne le dictionnaire pour avoir toujours les mêmes listes d'adjacences
    #(ordre alphabétique)
    dico = OrderedDict(sorted(dic.items(), key=lambda t: t[0]))
    r = 0
    identite = {}
    l = [[] for i in dico.keys()]
    for i in dico.keys():
        # ici on crée le dictionnaire qui donne un chiffre à chaque sommet
        identite[i] = r
        r += 1
    # on ordonne identite selon ses valeurs
    identite_trie = OrderedDict(sorted(identite.items(), key=lambda t: t[1]))
    for j in identite_trie.items():
        # pour chaque sommet du graphe on récupère la clef, le rang
        cle,rang = j
        for k in dico[cle].items():
            # pour chaque voisin de j on recupère sa cle et la valeur de l'arc
            clef,val = k
            (l[rang]).append((identite[clef],val))
    #l est la liste d'adjacence du graph et identite_trie est un dictionnaire qui associe
    #un chiffre à chaque sommet
    return(l,identite_trie)


def list_to_mat(l):
    n = len(l)
    mat = [[0 for i in range(0,n)] for i in range(0,n)]
    for i in range(0,n):
        #pour chaque sommet
        m = len(l[i])
        for j in range(0,m):
            #pour chaque voisin de ce sommet on récupère l'identifiant
            #et le poids de l'arc
            a,b = l[i][j]
            mat[i][a] = b
    return(mat)


def mat_to_list(mat):
    n = len(mat)
    l = [[] for i in range(0,n)]
    for i in range(0,n):
        for j in range(0,n):
            if mat[i][j] > 0 :
                (l[i]).append((j,mat[i][j]))
    return(l)


#Pour l'algorithme de Ford-Fulkerson on utilise le breadth first search :
inf = 999999999999
def BFS(g,s,p,pere):
    n = len(g)
    pere[s] = -1

    #pour savoir quels sommets ont été traités :
    visite = [] 
    for i in range(0,n):
        visite.append(False)
    visite[s] = True

    #la queue de stockage des sommets accessibles :
    queue = [] 
    queue.append(s)
    
    while len(queue) != 0 :
        u = queue.pop(0)
        for v in range(0,n):
            if visite[v] == False and g[u][v] > 0 :
            #si v est un voisin de u, non visité, alors :
                queue.append(v)
                visite[v] = True
                pere[v] = u

    #la boucle while s'arrête lorsque plus aucun sommet n'est accessible
    # et il suffit de vérifier si le puits a été visité :
    if visite[p]:
        return(True)
    else:
        return(False)


#fordfulk_path renvoie le flux max et les chemins ainsi que leurs flux max respectifs
def fordfulk_path(graph,source,puit):
    n = len(graph)
    g_prime = copy.deepcopy(graph)
    flux_max = 0
    #le tableau des parents permet de retrouver les chemins empruntés
    pere = [-1 for i in range(n)]
    paths = []
    #u et v sont des "pointeurs" 
    u,v = 0,0
    
    while BFS(g_prime,source,puit,pere) :
        flux = inf
        v = puit
        #la liste l permet de reconstruire le chemin de v à la source :
        l = [v]
        
        while v != source :
            #on "marche à reculons" en calculant le flux qui peut circuler
            #sur les arcs
            u = pere[v]
            l.insert(0,u)
            flux = min(flux,g_prime[u][v])
            v = pere[v]
            
        #on enregistre le chemin trouvé, son flux et v est réinitialisé
        paths.append((l,flux))
        v = puit
        #entre chaque BFS on réactualise le graph en tenant compte des
        #changements de la précédente boucle
        while v != source :
            u = pere[v]
            g_prime[u][v] -= flux
            g_prime[v][u] += flux
            v = pere[v]
        flux_max += flux
        
    return(flux_max,paths)         

#Théoriquement complexité en s^2 + s*a*(s + a) --> approximativement on est en O(s*a^2)



#chemins permet d'avoir les noms des sommets et pas juste leur chiffre dans identite :
def chemins(paths,identite):
    l = []
    #pour chaque chemin découvert
    for c in paths:
        path, flow = c
        n = len(path)
        l_prime = []
        #pour chaque sommet dans le chemin découvert
        for j in range(0,n):
            #on retrouve le nom du sommet dans le dictionnaire identite
            for cle,valeur in identite.items() :
                if valeur == path[j]:
                    l_prime.append(cle)
        l.append(l_prime)
    return(l)


#Ce troisième traitement a pour vocation de réduire le nombre de places inutiles dans les bus
#mais aussi de connaître combien d'usagers peut on intégrer au réseau.
#De plus, ces lignes peuvent servir en dehors du transport scolaire, l'algorithme de ford-fulkerson
#est donc très utile pour connaître les flux maximaux qu'il est possible d'avoir entre deux sommets
#quelconques du graph.


print("#########Exemple de Troisième Traitement#########")
#exemple:
bus,graph_oublie = nombre_bus_tot(semur_nord_est_poids,
                    [(18.5, ['montbard', 'crepand', 'montigny-monfort', 'champ-oiseau', 'semur']),
                     (27.5, ['fresnes', 'fain-les-montbards', 'seigny','les-granges','grignon','lantilly','villars','semur']),
                     (32.5, ['ampilly', 'gresigny', 'venarey', 'massigny', 'villenotte', 'semur']),
                     (36.5, ['laperriere', 'frolois', 'darcey', 'venarey', 'massigny', 'villenotte', 'semur']),
                     (35.5, ['verrey', 'gissey', 'venarey', 'massigny', 'villenotte', 'semur']),
                     (10.9, ['pouillenay', 'semur'])])

graph_flux = cumul_des_usagers(semur_nord_est,
                       semur_nord_est_poids,
                       [['montbard', 'crepand', 'montigny-monfort', 'champ-oiseau', 'semur'],
                        ['fresnes', 'fain-les-montbards', 'seigny','les-granges','grignon','lantilly','villars','semur'],
                        ['ampilly', 'gresigny', 'venarey', 'massigny', 'villenotte', 'semur'],
                        ['laperriere', 'frolois', 'darcey', 'venarey', 'massigny', 'villenotte', 'semur'],
                        ['verrey', 'gissey', 'venarey', 'massigny', 'villenotte', 'semur'],
                        ['pouillenay', 'semur']])

graph_capa = places_libres(bus,graph_flux)

graph_list,identite = dico_to_list(graph_capa)
graph_mat = list_to_mat(graph_list)
max_flow,path = fordfulk_path(graph_mat,identite['pouillenay'],identite['montbard'])
print(max_flow,chemins(path,identite))






           
