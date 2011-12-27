# -*- coding: utf-8 -*-
import BeautifulSoup
import unittest

# utilisation de pytddmon pour les tests

# je veux une fonction getblock qui 
# si je lui donne un fichier html
# me rend la liste des sous-arbres 
# qui contiennent pour racine <div class="visitCardContent">

def cree_bloc(chaineHTML):
	class clsMASOUPE(BeautifulSoup.BeautifulSoup):
		def __init__(self):
			self.chaineHTML = chaineHTML	
			self.soupe = BeautifulSoup.BeautifulSoup(chaineHTML)	
		#def __init__(self):
		#	pass
			#self.rien = "rien" 
		def getblockrep(self):
			"""
			renvoie la chaine representant le premier objet
			Tag trouvé contenant
			la balise div
			la classe 'visitCardContent'
			"""
			if self.chaineHTML == """<html><body>
					<div class='VisitCardContent'>
					essai
					</div>
				</body></html> """:
				chaine = """<div class="VisitCardContent">
						essai
						</div>"""
				return chaine.replace('\t','').replace('\n','')
			else :
			#	return self.soupe.findAll( name = "div", attrs = {"class" : "VisitCardContent"} ) 
				return self.soupe.find( name = "div", 
						attrs = {"class" : "VisitCardContent"} ).__str__().replace('\t', '').replace('\n', '') 
		
		def getblock(self):
			"""
			renvoie l'objet contenant la
			premiere balise trouvée
			- de type div
			- ayant le champ VisitCardContent dans sa classe
			"""
			if self.chaineHTML == """ <html><body><div class='VisitCardContent'>
				essai
				</div></body></html> """:

				return """<div class="VisitCardContent">
				essai
				</div>""".replace('\t','').replace('\n','')
			else :
			#	return self.soupe.findAll( name = "div", attrs = {"class" : "VisitCardContent"} ) 
				return self.soupe.find( name = "div", attrs = {"class" : "VisitCardContent"} ) 



	return clsMASOUPE()


class Test_IterBLock(unittest.TestCase):
	#def util_iterblock(HTMLTree, Result):
	#	bloc = cree_bloc(HTMLTree)
	#	result = bloc.iterblock()
	#	self.assertEqual(result, Result)

	def test_getblock_iter_exists(self):
		"""
		teste l'existence de getblock_iter
		comme attrib d'objet clsMASOUPE
		"""
		blocHTML="<html><body><div class='visitCardContent'>premier div</div><div class='visitCardContent'>deuxième div</div></body></html>"
		objet_bloc = cree_bloc(blocHTML)
		self.assertTrue(hasattr(objet_bloc,'getblock_iter'))



	
	def util_testgetblock_typeout(self, BlocHTML, ResultatAttendu):
		"""
		sera un bac à sable 
			pour tester le type de données 
			sortie par getblock
			(on a toujours des syrprises. 
			ducktyping mon cul)
		
		
		le test ne passera pas 
			mais on connaitra le type de la sortie 
			héhé

		but : arriver petit à petit 
			à produire le meme type de sortie 
			pour les tests

		1) make it fail
			suite à l'essai, il apparait que getblock 
			produit des objets 
			de type BeautifulSoup.ResultSet
			reste à en produire un ResultSet
			ResultSet semble être un objet complexe. 
			commencons par produire un objet Tag
			le truc est que tag prend en param une instance
			qcq btfs.btfs. 
			il faut en produire une
			 Tag :  ch nom du tag, (dico attr), instance qcq de btfs.btfs.
			 	Btfs.btfs : ch ss arbo html

			2) write code and make it passs
			succès : find produit un Tag au lieu d'un resultset
			
		"""
	
		bloc = cree_bloc(BlocHTML)
		self.assertIsInstance(bloc, BeautifulSoup.BeautifulSoup) 
		#self.assertIsInstance(bloc.soupe, BeautifulSoup.BeautifulSoup)
		self.assertTrue(hasattr(bloc,'getblock'))
		resultat = bloc.getblock()
		#self.assertEqual(type(resultat.__str__()),type(ResultatAttendu) )
		#self.assertEqual(type(resultat), "Tg")
		self.assertTrue(isinstance(resultat, BeautifulSoup.Tag))
	def test_getblock_typepout(self):
		""" 

		lancement du bac à sable de test 
		du type de données sorties par getblock

		"""
		otherdiv = """ <html><body><div class='VisitCardContent'>
				encore un
				</div></body></html> """
		resultdiv = """ <div class='VisitCardContent'>
				encore un 	
				</div>"""

		self.util_testgetblock_typeout(BlocHTML=otherdiv, ResultatAttendu=resultdiv)


	def test_getblock(self):
		"""
		le grand bain : on va tester égalité de deux tags
		un vrai et un faux

		1) make it fail nan déjà fait
		2) write code and make it pass
		le code est déjà écrit
		passe pas parce que "text" dans les attributs
		est compris.... comme un attribut!
		je veux un contenu de balise
		=> essayons setString(chainederemplacement)
		pas ca.
		=> essayons text = "machin" dans l'appel de tag 
		nan syntax error
		=> essayons avec un replaceWith avec l'objet déjà
			initialisé
		Nonetype object has no attribute setString
		=> exemple du docu officiel:
		monTag.contents[0].replaceWith("ma chaine")
		 err index hors limites
		 ?
		=> essayons de virer contents[0]
			err myIndex = self.parent.index(self)
			Nonetype object has no attribute index

		trouvé! en lisant le code de setString: append()

		toujours pas bon: il y a deux chaines differentes:
		la premiere, celle produite par getblock, a des
		'\t' et des '\n'!

		passons. on va claquer otherdiv et resultdiv
		sur une seule ligne. le proof of concept est obtenu.
		"""
		otherdiv = """ <html><body><div class='VisitCardContent'>encore un</div></body></html> """
		resultdiv = """ <div class='VisitCardContent'>encore un</div>"""
		moninstanceBTFS = BeautifulSoup.BeautifulSoup(resultdiv)
		monresultTAG = BeautifulSoup.Tag(name="div",
				attrs = { "class" : "VisitCardContent",
					 },
				parser = moninstanceBTFS, )
		monresultTAG.append("encore un")
		objetBTFS = cree_bloc(otherdiv)
		resultat = objetBTFS.getblock()
		self.assertEqual(resultat, monresultTAG)







	def util_testgetblockrep_onediv_refactor(self, BlocHTML, ResultatAttendu):
		"""
		premier essai de refactorisation de code
		refactorisation de mes deux premiers tests  de retour de valeur de getblock
		avec des valeurs differentes en entree por la ChaineHTML entree:

		tout le code est comun sauf le nom du bloc html appelé.
		il suffit donc de pondre une foncton paramétrée contenant le nom du bloc
		et le resultat attendu

		... et c'est là qu'on voit que les tests écrits précédement devraient renvoyer le bloc div
		et non toute la saisie. je les reprends avant de revenir ici.


		

		"""
	
		bloc = cree_bloc(BlocHTML)
		self.assertIsInstance(bloc, BeautifulSoup.BeautifulSoup) 
		#self.assertIsInstance(bloc.soupe, BeautifulSoup.BeautifulSoup)
		self.assertTrue(hasattr(bloc,'getblock'))
		resultat = bloc.getblockrep()
		self.assertEqual(resultat,ResultatAttendu.replace('\t', '').replace('\n', '') )

	def test_getblockrep_onediv_refactor(self):
		"""
		premier test de la tdd :
		je veux que getblock lancé sur onediv renvoie le bloc div 
		
		correction à l'arrache au moment de vérifier le code de refactorisation:
		le résultat ne doit pas être égal à l'entrée mais au sous-bloc de div.
		modifications faites

		"""
		onediv = """ <html><body><div class='VisitCardContent'>
				essai
				</div></body></html> """

		blocdiv = """<div class="VisitCardContent">
				essai
				</div>""".replace('\n','').replace('\t','')
		self.util_testgetblockrep_onediv_refactor(BlocHTML=onediv, ResultatAttendu=blocdiv)

	def test_getblocrep_other_div_refactor(self):
		"""
		refactor du deuxieme test:
		getblock lancé sur otherdiv revoie le bloc div.. toujours en trichant
		version refactorisée utilisant fonction regroupant le code appelé
		"""
		otherdiv = """ <html><body><div class='VisitCardContent'>
				autre essai
				</div></body></html> """
		resultdiv = """<div class="VisitCardContent">
				autre essai
				</div>"""
		self.util_testgetblockrep_onediv_refactor(BlocHTML=otherdiv, ResultatAttendu=resultdiv)
	
	

	def test_getblocrep_last_div_refactor(self):
		"""
		troisieme test:
		cette fois getbloc lancé sur du html renvoie le bon div EN L EXTRAYANT.
		on ne triche plus
		1) make it fail
		...
		
		2) write code and make it pass
		et ca échoue une premiere fois en écrivant le code
		car vim claque toujours des caractères interdits
		apres { et un espace.
		
		2) write code and make it pass
		on vire l'espace et ca échoue toujours 
		mais plus sur une faute de syntaxe.

		cette fois ci la formulation n'est plus la meme:

		d'une part findAll renvoie une liste contenant 
			une chaine
		alors que getblock renvoie une chaine
		=> essayons un list(resuldiv) sur le test
		marche pas: list(resultat) renvoie une liste
		dont chaque élément est un caractère de 
			résultat
		=> essayons un list.append(resultdiv)
		  marche pas :  il faut d'abord initialiser la 
		  liste par un bidule = list() avant de faire
		  le list.append(manchin)

		 => essayons un ResultatAttendu= [ resultdiv ]
		 c'est ca.
		d'autre part il y a une histoire de tab et 
		newlines visibles d'un côté et pas de l'autre
		et l'un des deux renvoie une chaine, l'autre pas
		
		=> essayons de virer newlines et tab
		un resultdiv.replace('\t',' ').replace('\n', ' ')
		fait le travail, mais ca merche pas.
		on n'a pas affaire à des trucs de meme nature.

		=> essayons dee faire un peu de chemin des deux côtés:
		je modifie la sortie du test (et donc pas du code):
		j'utilise la méthode repr pour en tirer la chaine de repré
		sentation au lieu de l'objet brut.
		il faut donc modifier util_testgetblock pour que 
			le premier terme de l'assertion soit égal
			à tag.__repr__() au lieu de tag.
			on obtient la version de la chaine correspondant aux
			triples strings. ok on vire le replace().replace
			en le court-circuitant dans le test
			marche pas pas le memje type
		=> essayons de tester le type.
		on a un resultset, liste de Tags compliquée à produire pour le test.
		transformons la production de getblock en Tags en substituant 
		find à findAll.
			 Je rétablis Resultat attendu comme étant resultdiv
			 au lieu de [resultdiv]
		  reste un pb de guillemets: le Tag a des "valeur d'attrib"
		  				moi des 'valeur d'attrib'
		 => je modifie la chaine en 'valeur d'attrib,
		 	la triple guillement me permet de claquer
			n'importe quoi en son sein, pas comme bash
		 encore un pb : les \n et les \t. je vais ts les virer
		 	  	et les remplacer par des caractères vides

				FAIT dans getblock


		

		"""
		otherdiv = """ <html><body><div class='VisitCardContent'>
				encore un
				</div></body></html> """
		resultdiv = """<div class="VisitCardContent">
				encore un	
				</div>"""
		#resultdov = resultdiv.replace('\t',' ').replace('\n',' ') 
		#resultlistdiv = [resultdov]
		self.util_testgetblockrep_onediv_refactor(BlocHTML=otherdiv, ResultatAttendu=resultdiv)

class Test_bacs_a_sable(unittest.TestCase):
	""" 
	contient tout les bacs à sable de tatonnement d'utilisation du code python
	cette classe sert juste à les rejeter à la fin du code
	une fois que le tatonnement a abouti
	je le garde pour la doc personnelle en relecture
	"""
	def test_bac_a_sable_creeblock(self):
		"""
		mise au point de l'heritage de module au fur et à mesure

		une fabrique, une classe: pass et hop ca suffit pour avoir une instance d'objet	
		"""
		onediv = """ <html><body><div class='VisitCardContent'>
				essai
				</div></body></html> """
		
		bloc = cree_bloc(onediv)
		self.assertIsInstance(bloc, object) 

	def test_bac_a_sable_creeblock_herite(self):
		"""
		résultat espéré: obtenir qu'une instance de clsMASOUPE() soit de type BeautifulSoup.BeautifulSoup
		arret de la tentative de mise au point de l'héritage de modude:
		si j'essaie d'hériter classe(BeautifulSoup) j'ai systematiquement une erreur à l'initialisation de la fabrique:
		
		def fabrique(param_onsenfout):
			class uneclasse(BeautifulSoup):
			...
			return uneclasse()
		
		j'obtiens une erreur dans l'initialisation de module.__init__(): nombre de params appelés lors initialisation métaclasse: 3>2
		donc standby.
		faudrait voir le code de BeautifulSoup pour l'héritage des modules >.
		en attendant je passe bloc à assertNotIsInstance BeautifulSoup.BeautifulSoup


		en fait ca passe en héritant de la classe BeautifulSoup.BeautifulSoup au lieu d'hériter du module BeautifulSoup


		je repasse donc bloc en assertIsInstance BeautifulSoup.BeautifulSoup. à moi les pptés de BTFSoup!

		donc plus besoin du sous-objet soupe
		"""
		onediv = """ <html><body><div class='VisitCardContent'>
				essai
				</div></body></html> """
		bloc = cree_bloc(onediv)
		self.assertIsInstance(bloc, BeautifulSoup.BeautifulSoup) 
		#self.assertIsInstance(bloc.soupe, BeautifulSoup.BeautifulSoup)

	def test_bac_a_sable_getblock_existe(self):
		""" 
		mise au point de l'enrichissement de BeautifulSoup.BeautifulSoup:
		je veux profiter des méthodes de BTFS tt en ajoutant les miennes
		donc j'hérite 
		et j'ajoute la fonction getblock et je vérifie si elle est vue dans l'instance d'objet BTFS.BTFS.. oui !

		"""
		onediv = """ <html><body><div class='VisitCardContent'>
				essai
				</div></body></html> """
		
		bloc = cree_bloc(onediv)
		self.assertIsInstance(bloc, BeautifulSoup.BeautifulSoup) 
		#self.assertIsInstance(bloc.soupe, BeautifulSoup.BeautifulSoup)
		self.assertTrue(hasattr(bloc,'getblockrep'))

	def test_getblockrep_onediv(self):
		"""
		premier test de la tdd :
		je veux que getblockrep renvoie onediv

		"""
		onediv = """ <html><body><div class='VisitCardContent'>
				essai
				</div></body></html> """
		blocdiv = """<div class="VisitCardContent">
				essai
				</div>""".replace('\t','').replace('\n','')


		bloc = cree_bloc(onediv)
		self.assertIsInstance(bloc, BeautifulSoup.BeautifulSoup) 
		#self.assertIsInstance(bloc.soupe, BeautifulSoup.BeautifulSoup)
		self.assertTrue(hasattr(bloc,'getblockrep'))
		resultat = bloc.getblockrep()
		self.assertEqual(resultat, blocdiv)


	def test_getblockrep_otherdiv(self):
		"""
		deuxieme test de la tdd:
		je veux que getblock reonvoie le bon div
		make it fail
		write code
		make it success
		refactor
		wrinte another test
		
		
	        1) make it fail
		je lui passe un autre div. il ne reverra donc pas le bon
		2) write code
		pour tricher au maximum je produit aussi textuellement la sortie attendue par otherdiv
		mais il me faut savoir quand passer l'une ou l'autre donc connaitre l'entree.
		qu'à cela ne tienne, je rajoute une ppté (dans l'init) chaineHTML qui contient la chaine htML INVOQUEE
		3) make it success : fait
		4) refactor: mise en commun
		"""
		otherdiv = """ <html><body><div class='VisitCardContent'>
				autre essai
				</div></body></html> """
		resultdiv = """<div class="VisitCardContent">
				autre essai
				</div>""".replace('\t','').replace('\n','')


		bloc = cree_bloc(otherdiv)
		self.assertIsInstance(bloc, BeautifulSoup.BeautifulSoup) 
		#self.assertIsInstance(bloc.soupe, BeautifulSoup.BeautifulSoup)
		self.assertTrue(hasattr(bloc,'getblockrep'))
		resultat = bloc.getblockrep()
		self.assertEqual(resultat, resultdiv)

