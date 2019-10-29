import time

class Card :
    """ Classe reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sentant les cartes d'un jeu classique de 54 cartes.
    """
    VALUES = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    COLORS = ["\u2665","\u2660","\u2663","\u2666"] # Hearts,Spades,Clubs,Diamonds

    def __init__(self,value,color) :
        self.value=value
        self.color=color

    def __str__(self) :
        """ Fonction pour la reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sentation graphique """
        return self.VALUES[self.value]+self.COLORS[self.color]

    def get_remaining_cards(used_cards) :
        """ Retourne l'ensemble des cartes sauf celles prÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sentes dans l'ensemble used_cards
        """
        res=[]
        for i in range(0,13) :
            for j in range(0,4) :
                c = Card(i,j)
                if not(c in used_cards) :
                    res.append(Card(i,j))
        return res

    """ Fonctions pour la comparaison des cartes (utilisÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es dans la gestion des mains)
    """
    def __lt__(self, other)  : # For x < y
        return self.value < other.value or (self.value == other.value and self.color < other.color)
    def __le__(self, other)  : # For x <= y
        return self.value < other.value or (self.value == other.value and self.color <= other.color)
    def __eq__(self, other)  : # For x == y
        return self.value == other.value and self.color == other.color
    def __ne__(self,other) : # For x != y
        return not(self == other)
    def __gt__(self, other)  : # For x > y
        return not(self <= other)
    def __ge__(self, other)  : # For x >= y
        return not(self < other)

class HoleCards :
    """ Classe reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sentant les 2 cartes du joueur
    """

    def __init__(self,card1,card2) :
        if card1 > card2 :
            self.card1=card1
            self.card2=card2
        else :
            self.card1=card2
            self.card2=card1

    def __str__(self) :
        """ Fonction pour la reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sentation graphique """
        return "("+str(self.card1)+","+str(self.card2)+")"

class CardValue :
    """ Classe interne pour la comparaison des mains
    """
    def __init__(self,number,value) :
        self.number = number
        self.value = value

    def __lt__(self, other)  : # For x < y
        return self.number < other.number or (self.number == other.number and self.value < other.value)
    def __le__(self, other)  : # For x <= y
        return self.number < other.number or (self.number == other.number and self.value <= other.value)
    def __eq__(self, other)  : # For x == y
        return self.value == other.value and self.number == other.number
    def __ne__(self,other) : # For x != y
        return not(self == other)
    def __gt__(self, other)  : # For x > y
        return not(self <= other)
    def __ge__(self, other)  : # For x >= y
        return not(self < other)

class Hand :
    """ Classe reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sentant une main (5 cartes)
    """
    def __init__(self,cards) :
        self.cards = cards
        self.cards.sort()

    def is_all_same_color(self) :
        """ Fonction interne """
        c = self.cards[0].color
        for i in range(1,5) :
            if self.cards[i].color != c :
                return False
        return True

    def is_following_values(self) :
        """ Fonction interne """
        ## test if straight with Ace after King
        straight_ace_after_king = self.cards[0].value==0
        for i in range(1,5) :
            if self.cards[i].value != (8+i) :
                straight_ace_after_king = False
                break
        if straight_ace_after_king :
            return True
        ## others cases
        for i in range(1,5) :
            if self.cards[i].value != (self.cards[i-1].value+1) :
                return False
        return True

    def get_cards_values(self) :
        """ Fonction interne """
        values = [0]*14
        res=[]
        for c in self.cards :
            values[(c.value+13)%14]+=1
        for i in range(1,14) :
            if values[i]!=0 :
                res.append(CardValue(values[i],i))
        res.sort(reverse=True)
        return res

    def get_St_value(self) :
        """ Fonction interne """
        if self.cards[0].value == 0 and self.cards[4].value==12 :
            return 13
        else :
            return self.cards[4].value

    def get_hand_value(self) :
        """ Fonction interne """
        if self.is_straight_flush() :
            return (9,self.get_St_value())
        if self.is_four_of_a_kind() :
            return (8,self.get_cards_values())
        if self.is_full_house() :
            return (7,self.get_cards_values())
        if self.is_flush() :
            return (6,self.get_cards_values())
        if self.is_straight() :
            return (5,self.get_cards_values())
        if self.is_three_of_a_kind() :
            return (4,self.get_cards_values())
        if self.is_two_pairs() :
            return (3,self.get_cards_values())
        if self.is_pair() :
            return (2,self.get_cards_values())
        else :
            return (1,self.get_cards_values())

    def is_straight_flush(self) :
        """ teste si la main est une quinte flush """
        return self.is_all_same_color() and self.is_following_values()

    def is_flush(self) :
        """ teste si la main est une couleur """
        return self.is_all_same_color() and not(self.is_following_values())

    def is_straight(self) :
        """ teste si la main est une suite """
        return not(self.is_all_same_color()) and self.is_following_values()

    def is_four_of_a_kind(self) :
        """ teste si la main est un carrÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© """
        values = [0]*13
        for c in self.cards :
            values[c.value]+=1
        for i in values :
            if i==4 :
                return True
        return False

    def is_full_house(self) :
        """ teste si la main est un full """
        values = [0]*13
        for c in self.cards :
            values[c.value]+=1
        pair = False
        three_of_a_kind = False
        for i in values :
            if i==3 :
                three_of_a_kind = True
            if i==2 :
                pair = True
        return pair and three_of_a_kind

    def is_three_of_a_kind(self) :
        """ teste si la main est un brelan """
        values = [0]*13
        for c in self.cards :
            values[c.value]+=1
        three_of_a_kind = False
        for i in values :
            if i==3 :
                three_of_a_kind = True
            if i==2 :
                return False
        return three_of_a_kind

    def is_two_pairs(self) :
        """ teste si la main est deux paires """
        values = [0]*13
        for c in self.cards :
            values[c.value]+=1
        pair = False
        for i in values :
            if i==2 :
                if pair :
                    return True
                else :
                    pair = True
        return False

    def is_pair(self) :
        """ teste si la main est une paire """
        values = [0]*13
        for c in self.cards :
            values[c.value]+=1
        pair = False
        for i in values :
            if i==3 :
                return False
            if i==2 :
                if pair :
                    return False
                else :
                    pair = True
        return pair

    def __str__(self) :
        res = "("+str(self.cards[0])+","+str(self.cards[1])+","+str(self.cards[2])+","
        res+= str(self.cards[3])+","+str(self.cards[4])+")"
        return res

    def __lt__(self,other) :
        """ teste si la main est < other """
        if other == None :
            return False
        a,b = self.get_hand_value()
        aa,bb = other.get_hand_value()
        return a<aa or (a==aa and b < bb)

    def __le__(self,other) :
        """ teste si la main est <= other """
        if other == None :
            return False
        a,b = self.get_hand_value()
        aa,bb = other.get_hand_value()
        return a<aa or (a==aa and b <= bb)

    def __eq__(self,other) :
        """ teste si la main est == other """
        if other == None :
            return False
        a,b = self.get_hand_value()
        aa,bb = other.get_hand_value()
        return a==aa and b == bb

    def __ne__(self,other) :
        """ teste si la main est != other """
        return not(self == other)

    def __gt__(self, other)  :
        """ teste si la main est > other """
        return not(self <= other)

    def __ge__(self, other)  :
        """ teste si la main est >= other """
        return not(self < other)

class GameSituation :
    """ Classe reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sentant l'ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©tat du jeu :
        - hole_cards        : reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sente les cartes cachÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©es du joueur
        - community_cards   : reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sente les cartes communes sur la table
    """
    def __init__(self,hole_cards,community_cards) :
        self.hole_cards = hole_cards
        self.community_cards = community_cards

    def get_best_hand(self) :
        """ Fonction retournant la meilleure main possible parmi les 7 cartes : 2 du joueur et 5 communes
            ATTENTION ! : ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â  n'utiliser que s'il y a effectivement 5 cartes communes
        """
        if len(self.community_cards) != 5 :
            raise NameError("get_best_hand")
        cards_set = [self.hole_cards.card1,self.hole_cards.card2]
        cards_set.extend(self.community_cards)
        best_hand = None
        for i in range(0,len(cards_set)-1) :
            for j in range(i+1,len(cards_set)) :
                c_s = cards_set[0:i]
                c_s.extend(cards_set[i+1:j])
                c_s.extend(cards_set[j+1:len(cards_set)])
                h = Hand(c_s)
                if h > best_hand :
                    best_hand = h
        return best_hand

    def get_probabilities_after_river(self) :
        main_cards=[self.hole_cards.card1,self.hole_cards.card2]
        main_cards.extend(self.community_cards)
        game = GameSituation(self.hole_cards,self.community_cards)
        others = Card.get_remaining_cards(main_cards)
        probA = 0
        probB = 0
        probC = 0
        n = 0

        first = game.get_best_hand()
        for i in range (0,len(others)):
            for j in range (i+1,len(others)) :
                n += 1
                cardp2 = HoleCards(others[i], others[j])
                game2 = GameSituation(cardp2, c_c)
                if(first > game2.get_best_hand()) :
                    probA+=1
                elif (first == game2.get_best_hand()):
                    probB+=1
                elif (first < game2.get_best_hand()):
                    probC +=1
        a = probA/n
        b = probB/n
        c = probC/n

        return a,b,c


        """ ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ complÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ter !
            Fonction retournant 3 nombres rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©els (a,b,c) oÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¹
            - a : reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sente la probabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© que le joueur gagne contre un autre joueur aprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s la river
            - b : reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sente la probabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© que le joueur fasse nul contre un autre joueur aprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s la river
            - c : reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sente la probabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© que le joueur perdre contre un autre joueur aprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s la river
        """

    def get_probabilities_after_turn(self) :

        main_cards=[self.hole_cards.card1,self.hole_cards.card2] #CrÃƒÂ©ation de la main
        main_cards.extend(self.community_cards) #Ajouter ÃƒÂ  cette main les cartes du plateau
        game = GameSituation(self.hole_cards,self.community_cards) # On crÃƒÂ©ÃƒÂ© la situation avec nos cartes et toutes les cartes
        others = Card.get_remaining_cards(main_cards) # recupÃƒÂ©rer les cartes restantes en fonction de nos cartes
        probA = 0
        probB = 0
        probC = 0
        n = 0 #compter les instances pour rÃƒÂ©cupÃƒÂ©rer le cardinal
        for cardRiver in others:
            community_cards_Potentiel=[]
            card_used=[]
            community_cards_Potentiel.extend(self.community_cards)
            community_cards_Potentiel.append(cardRiver)
            card_used.extend(community_cards_Potentiel)
            card_used.append(self.hole_cards.card1)
            card_used.append(self.hole_cards.card2)
            cartPossible=[]
            cartPossible = Card.get_remaining_cards(card_used)
            first = GameSituation(self.hole_cards,community_cards_Potentiel)
            besthand=first.get_best_hand()

            for i in others: #voir pour les cartes de l'autre joueur
                for j in others :
                    n += 1
                    cardp2 = HoleCards(i, j) #on teste avec des mains diffÃƒÂ©rentes
                    game2 = GameSituation(cardp2, community_cards_Potentiel)
                    mainpot = game2.get_best_hand()
                    if(first > mainpot) : #compare entre le premier et deuxiÃƒÂ¨me
                        probA+=1
                    elif (first == mainpot):
                        probB+=1
                    elif (first < mainpot):
                        probC +=1

        a = probA/n
        b = probB/n
        c = probC/n








        """ ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ complÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ter !
            Fonction retournant 3 nombres rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©els (a,b,c) oÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¹
            - a : reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sente la probabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© que le joueur gagne contre un autre joueur aprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s le turn
            - b : reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sente la probabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© que le joueur fasse nul contre un autre joueur aprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s le turn
            - c : reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sente la probabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© que le joueur perdre contre un autre joueur aprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s le turn
        """
        return a,b,c

    def get_probabilities_after_flop(self) :

        """ ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ complÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©ter !
            Fonction retournant 3 nombres rÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©els (a,b,c) oÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¹
            - a : reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sente la probabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© que le joueur gagne contre un autre joueur aprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s le flop
            - b : reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sente la probabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© que le joueur fasse nul contre un autre joueur aprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s le flop
            - c : reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sente la probabilitÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â© que le joueur perdre contre un autre joueur aprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¨s le flop
        """
        return 0,0,0

    def get_probabilities(self) :
        n = len(self.community_cards)
        if n == 5 :
            return self.get_probabilities_after_river()
        elif n == 4 :
            return self.get_probabilities_after_turn()
        elif n == 3 :
            return self.get_probabilities_after_flop()

    def __str__(self) :
        """ Fonction pour la reprÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â©sentation graphique """
        res = "HC : "+str(self.hole_cards)+" , CC = ("
        for c in self.community_cards :
            res+=str(c)+","
        return res[:-1]+")"


h1=Hand([Card(0,1),Card(9,1),Card(10,1),Card(11,1),Card(12,1)])
h2=Hand([Card(3,2),Card(3,3),Card(3,0),Card(3,1),Card(6,1)])
h3=Hand([Card(3,2),Card(3,1),Card(3,0),Card(7,1),Card(7,3)])
h4=Hand([Card(1,2),Card(3,2),Card(8,2),Card(9,2),Card(0,2)])
h5=Hand([Card(5,2),Card(6,3),Card(7,0),Card(9,1),Card(8,1)])
h6=Hand([Card(6,2),Card(6,3),Card(6,0),Card(3,1),Card(10,1)])
h7=Hand([Card(10,2),Card(10,3),Card(12,0),Card(12,1),Card(4,1)])
h8=Hand([Card(0,2),Card(0,3),Card(2,0),Card(8,1),Card(9,1)])
h9=Hand([Card(1,2),Card(5,3),Card(6,0),Card(8,1),Card(11,1)])


hands = [h1,h2,h3,h4,h5,h6,h7,h8,h9]

print("Est-ce que "+str(h1)+" > "+str(h2)+" : "+str(h1 > h2))
print("Est-ce que "+str(h3)+" == "+str(h4)+" : "+str(h3 == h4))
print("Est-ce que "+str(h5)+" >= "+str(h6)+" : "+str(h5 >= h6))
print("Est-ce que "+str(h7)+" < "+str(h8)+" : "+str(h7 < h8))
print("Est-ce que "+str(h9)+" != "+str(h1)+" : "+str(h9 != h1))


h_c = HoleCards(Card(1,0),Card(4,1))
c_c = [Card(3,3),Card(2,1),Card(5,3),Card(10,2)]
#,Card(11,1)

gs = GameSituation(h_c,c_c)
print(gs)

#best_hand = gs.get_best_hand()
#print("Best hand : "+str(best_hand))

start_time = time.time()
print(gs.get_probabilities())
print("--- %s seconds ---" % (time.time() - start_time))

