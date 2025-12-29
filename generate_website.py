import pandas as pd
import json
from collections import OrderedDict

# Read Excel file
xls = pd.ExcelFile('menu.xlsx')

# Mapping of sheet names to page names and URLs
pages = {
    'AgraharaRuchulu': {
        'title': 'Agrahara Ruchulu',
        'filename': 'agrahara-ruchulu.html',
        'url': 'agrahara-ruchulu.html'
    },
    'GunturKaaram': {
        'title': 'Guntur Kaaram',
        'filename': 'guntur-kaaram.html',
        'url': 'guntur-kaaram.html'
    },
    'Aritaaku': {
        'title': 'Aritaaku',
        'filename': 'aritaaku.html',
        'url': 'aritaaku.html'
    }
}

def escape_html(text):
    """Escape HTML special characters"""
    if pd.isna(text):
        return ""
    text = str(text)
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))

def create_category_key(category):
    """Create a key from category name"""
    return category.lower().replace(' ', '_').replace('&', 'and').replace('/', '_').strip()

# Comprehensive Telugu translations for categories
CATEGORY_TRANSLATIONS = {
    'biryani': {'en': 'Biryani', 'te': 'బిర్యాని'},
    'combo_rice_bowls': {'en': 'Combo Rice Bowls', 'te': 'కాంబో రైస్ బౌల్స్'},
    'fried_rice': {'en': 'Fried Rice', 'te': 'ఫ్రైడ్ రైస్'},
    'pulav': {'en': 'Pulav', 'te': 'పులావ్'},
    'rice_bowls': {'en': 'Rice Bowls', 'te': 'రైస్ బౌల్స్'},
    'roti_combo': {'en': 'Roti Combo', 'te': 'రొటీ కాంబో'},
    'pickles': {'en': 'Pickles', 'te': 'ఊరగాయలు'},
    'powders': {'en': 'Powders', 'te': 'పొడులు'},
    'curd_varieties': {'en': 'Curd Varieties', 'te': 'పెరుగు రకాలు'},
    'curries': {'en': 'Curries', 'te': 'కూరలు'},
    'dal': {'en': 'Dal', 'te': 'పప్పు'},
    'desserts': {'en': 'Desserts', 'te': 'మిఠాయిలు'},
    'roti_pacchadi': {'en': 'Roti Pacchadi', 'te': 'రొటీ పచ్చడి'},
    'snacks': {'en': 'Snacks', 'te': 'చిరుతిండిపదార్థాలు'},
    'stew': {'en': 'Stew', 'te': 'స్టూలు'},
}

# Comprehensive Telugu translations for menu items
ITEM_TRANSLATIONS = {
    # Agrahara Ruchulu - Rice Bowls
    'G3 Ghee Guntur Gongura Annam': {'en': 'G3 Ghee Guntur Gongura Annam', 'te': 'జీ3 నెయ్యి గుంటూర్ గోంగూర అన్నం'},
    'Ghee Muddapappu Avakai Annam': {'en': 'Ghee Muddapappu Avakai Annam', 'te': 'నెయ్యి ముద్దపప్పు ఆవకాయ అన్నం'},
    'Amaravati Daddojanam': {'en': 'Amaravati Daddojanam', 'te': 'అమరావతి దధ్యోజనం'},
    'Kandi Podi Magaya Annam': {'en': 'Kandi Podi Magaya Annam', 'te': 'కంది పొడి మాగాయ అన్నం'},
    'Ghee Palli Podi Rice': {'en': 'Ghee Palli Podi Rice', 'te': 'నెయ్యి పల్లి పొడి అన్నం'},
    'Nellore Pappu Charu Annam': {'en': 'Nellore Pappu Charu Annam', 'te': 'నెల్లూరు పప్పు చారు అన్నం'},
    'R3-Rajamundry Rasam Rice': {'en': 'R3-Rajamundry Rasam Rice', 'te': 'ఆర్3-రాజమండ్రి రసం అన్నం'},
    'Ghee Muddapappu Pandumirchi Rice': {'en': 'Ghee Muddapappu Pandumirchi Rice', 'te': 'నెయ్యి ముద్దపప్పు పండుమిర్చి అన్నం'},
    'Karivepaku Rice': {'en': 'Karivepaku Rice', 'te': 'కరివేపాకు అన్నం'},
    'Guntur Gongura Pulihora': {'en': 'Guntur Gongura Pulihora', 'te': 'గుంటూర్ గోంగూర పులిహోర'},
    'Lemon Rice': {'en': 'Lemon Rice', 'te': 'నిమ్మకాయ పులిహోర'},
    'Mango Pulihora': {'en': 'Mango Pulihora', 'te': 'మామిడి పులిహోర'},
    'Chintapandu Pulihora': {'en': 'Chintapandu Pulihora', 'te': 'చింతపండు పులిహోర'},
    'Muddapappu Pachi pulusu': {'en': 'Muddapappu Pachi pulusu', 'te': 'ముద్దపప్పు పచ్చి పులుసు'},
    'Tomato Rice': {'en': 'Tomato Rice', 'te': 'టమాట అన్నం'},
    'Vangi Bath': {'en': 'Vangi Bath', 'te': 'వంగి బాత్'},
    'Pudina Rice': {'en': 'Pudina Rice', 'te': 'పుదీనా అన్నం'},
    'Bengaluru Bisibele Bath': {'en': 'Bengaluru Bisibele Bath', 'te': 'బెంగళూరు బిసిబెలె బాత్'},
    'Chitti Avakay Muddapappu Rice': {'en': 'Chitti Avakay Muddapappu Rice', 'te': 'చిట్టి ఆవకాయ ముద్దపప్పు అన్నం'},
    'Sambar Rice': {'en': 'Sambar Rice', 'te': 'సాంబార్ అన్నం'},
    
    # Biryani
    'Veg Dum Biryani': {'en': 'Veg Dum Biryani', 'te': 'వెజ్ డమ్ బిర్యాని'},
    'Kaju Panner Biryani': {'en': 'Kaju Panner Biryani', 'te': 'కాజు పనీర్ బిర్యాని'},
    'Ulavacharu Veg Biryani': {'en': 'Ulavacharu Veg Biryani', 'te': 'ఉలవచారు వెజ్ బిర్యాని'},
    'Dondakaya Ulli kaaram Biryani': {'en': 'Dondakaya Ulli kaaram Biryani', 'te': 'దొండకాయ ఉల్లి కారం బిర్యాని'},
    'Veg Donne Biryani': {'en': 'Veg Donne Biryani', 'te': 'వెజ్ దొన్నె బిర్యాని'},
    'Gundamma Guttivankaya Biryani': {'en': 'Gundamma Guttivankaya Biryani', 'te': 'గుండమ్మ గుట్టివంకాయ బిర్యాని'},
    'Cut Mirchi Biryani': {'en': 'Cut Mirchi Biryani', 'te': 'కట్ మిర్చి బిర్యాని'},
    'Pesara Punugula Biryani': {'en': 'Pesara Punugula Biryani', 'te': 'పెసర పునుగుల బిర్యాని'},
    'Panasakaya Biryani': {'en': 'Panasakaya Biryani', 'te': 'పనసకాయ బిర్యాని'},
    
    # Combo Rice Bowls
    'Ghee Pongal + Palli Chutney': {'en': 'Ghee Pongal + Palli Chutney', 'te': 'నెయ్యి పొంగళ్ + పల్లి చట్నీ'},
    'Ghee Sambar Rice+Potato Fry': {'en': 'Ghee Sambar Rice+Potato Fry', 'te': 'నెయ్యి సాంబార్ అన్నం+ఉర్లగడ్డ వేపుడు'},
    'Jeera Rice + Panner Butter Masala': {'en': 'Jeera Rice + Panner Butter Masala', 'te': 'జీర ధనియాలు అన్నం + పనీర్ వెన్న మసాలా'},
    'Jeera Rice + Dal Tadka': {'en': 'Jeera Rice + Dal Tadka', 'te': 'జీర ధనియాలు అన్నం + పప్పు తడక'},
    'Pappu Charu Annam +Potato Fry': {'en': 'Pappu Charu Annam +Potato Fry', 'te': 'పప్పు చారు అన్నం+ఉర్లగడ్డ వేపుడు'},
    'Coconut Rice + Aloo Curry': {'en': 'Coconut Rice + Aloo Curry', 'te': 'కొబ్బరి అన్నం + ఉర్లగడ్డ కూర'},
    'Jeera Rice + Kadhai Panner': {'en': 'Jeera Rice + Kadhai Panner', 'te': 'జీర ధనియాలు అన్నం + కడ్హాయి పనీర్'},
    'Coconut Rice + Aloo Kurma': {'en': 'Coconut Rice + Aloo Kurma', 'te': 'కొబ్బరి అన్నం + ఉర్లగడ్డ కుర్మా'},
    'Peas Pulav+Aloo Kurma': {'en': 'Peas Pulav+Aloo Kurma', 'te': 'బటాణి పులావ్+ఉర్లగడ్డ కుర్మా'},
    
    # Fried Rice
    'Vegetable Fried Rice': {'en': 'Vegetable Fried Rice', 'te': 'కూరగాయలు వేయించిన అన్నం'},
    'Avakaya Fried Rice': {'en': 'Avakaya Fried Rice', 'te': 'ఆవకాయ వేయించిన అన్నం'},
    'Panner Fried Rice': {'en': 'Panner Fried Rice', 'te': 'పనీర్ వేయించిన అన్నం'},
    'Burnt Garlic Fried Rice': {'en': 'Burnt Garlic Fried Rice', 'te': 'వెల్లుల్లి వేయించిన అన్నం'},
    
    # Pulav
    'Pacchimirchi Veg Pulav': {'en': 'Pacchimirchi Veg Pulav', 'te': 'పచ్చిమిర్చి వెజ్ పులావ్'},
    'Peas Pulav': {'en': 'Peas Pulav', 'te': 'బటాణి పులావ్'},
    'Soya Pulav': {'en': 'Soya Pulav', 'te': 'సోయా పులావ్'},
    'P4-Palnadu Pacchimirchi Panner Pulav': {'en': 'P4-Palnadu Pacchimirchi Panner Pulav', 'te': 'పీ4-పాలనాడు పచ్చిమిర్చి పనీర్ పులావ్'},
    'Mixed Veg Pulav': {'en': 'Mixed Veg Pulav', 'te': 'మిశ్రమ కూరగాయలు పులావ్'},
    'Chikkudu Kaaya Pulav': {'en': 'Chikkudu Kaaya Pulav', 'te': 'చిక్కుడు కాయ పులావ్'},
    'Gongura Pulav': {'en': 'Gongura Pulav', 'te': 'గోంగూర పులావ్'},
    'Gundamma Guttivankaya Pulav': {'en': 'Gundamma Guttivankaya Pulav', 'te': 'గుండమ్మ గుట్టివంకాయ పులావ్'},
    'Kaju Panner Pulav': {'en': 'Kaju Panner Pulav', 'te': 'కాజు పనీర్ పులావ్'},
    'Gongura Paneer Pulav': {'en': 'Gongura Paneer Pulav', 'te': 'గోంగూర పనీర్ పులావ్'},
    'Kaju Pulao': {'en': 'Kaju Pulao', 'te': 'కాజు పులావ్'},
    'Tomato Pulav': {'en': 'Tomato Pulav', 'te': 'టమాట పులావ్'},
    
    # Roti Combo
    'Chapathi + Aloo Tomato Curry': {'en': 'Chapathi + Aloo Tomato Curry', 'te': 'చపాతి + ఉర్లగడ్డ టమాట కూర'},
    'Chapathi + Panner Butter Masala': {'en': 'Chapathi + Panner Butter Masala', 'te': 'చపాతి + పనీర్ వెన్న మసాలా'},
    'Chapathi + Dal Fry': {'en': 'Chapathi + Dal Fry', 'te': 'చపాతి + పప్పు వేపుడు'},
    'Chapathi + Chole Curry': {'en': 'Chapathi + Chole Curry', 'te': 'చపాతి + చోలె కూర'},
    'Chapathi + Gutti Vankaya Curry': {'en': 'Chapathi + Gutti Vankaya Curry', 'te': 'చపాతి + గుట్టి వంకాయ కూర'},
    'Chapathi + MoongDal Curry': {'en': 'Chapathi + MoongDal Curry', 'te': 'చపాతి + పెసరపప్పు కూర'},
    'Chapathi + Aloo Cauliflower Curry': {'en': 'Chapathi + Aloo Cauliflower Curry', 'te': 'చపాతి + ఉర్లగడ్డ ఫ్లవర్ కూర'},
    'Chapathi + Palak Panner Curry': {'en': 'Chapathi + Palak Panner Curry', 'te': 'చపాతి + పాలకూర పనీర్ కూర'},
    'Chapathi + Boondi Curry': {'en': 'Chapathi + Boondi Curry', 'te': 'చపాతి + బూంది కూర'},
    'Chapathi + Pesara Punugula Curry': {'en': 'Chapathi + Pesara Punugula Curry', 'te': 'చపాతి + పెసర పునుగుల కూర'},
    'Chapathi+ Aloo Matar Curry': {'en': 'Chapathi+ Aloo Matar Curry', 'te': 'చపాతి+ ఉర్లగడ్డ మట్టర్ కూర'},
    'Chapathi+ Mixed Veg Curry': {'en': 'Chapathi+ Mixed Veg Curry', 'te': 'చపాతి+ మిశ్రమ కూరగాయలు కూర'},
    'Chapathi+ Aloo Kurma': {'en': 'Chapathi+ Aloo Kurma', 'te': 'చపాతి+ ఉర్లగడ్డ కుర్మా'},
    
    # Guntur Kaaram - Pickles
    'Tomato': {'en': 'Tomato', 'te': 'టమాట ఊరగాయ'},
    'Ginger ( Allam )': {'en': 'Ginger ( Allam )', 'te': 'అల్లం ఊరగాయ'},
    'Lemon ( Nimmakaya )': {'en': 'Lemon ( Nimmakaya )', 'te': 'నిమ్మకాయ ఊరగాయ'},
    'Small Cut Mango(Chitti Mukkala Avakaya)': {'en': 'Small Cut Mango(Chitti Mukkala Avakaya)', 'te': 'చిట్టి ముక్కల ఆవకాయ'},
    'Cilantro (Kothimeera)': {'en': 'Cilantro (Kothimeera)', 'te': 'కొత్తిమీర ఊరగాయ'},
    'Bittergourd (Kakarakaya Avakaya)': {'en': 'Bittergourd (Kakarakaya Avakaya)', 'te': 'కాకరకాయ ఆవకాయ'},
    'Dosa Avakaya': {'en': 'Dosa Avakaya', 'te': 'దోస ఆవకాయ'},
    'Cauliflower': {'en': 'Cauliflower', 'te': 'ఫ్లవర్ ఊరగాయ'},
    'Mango Thokku': {'en': 'Mango Thokku', 'te': 'మామిడి ఠొక్కు'},
    
    # Powders
    'Kandi Podi': {'en': 'Kandi Podi', 'te': 'కంది పొడి'},
    'Senaga Podi': {'en': 'Senaga Podi', 'te': 'సెనగ పొడి'},
    'Kobbari Podi': {'en': 'Kobbari Podi', 'te': 'కొబ్బరి పొడి'},
    'Karam Podi': {'en': 'Karam Podi', 'te': 'కారం పొడి'},
    'Karivepaku Podi': {'en': 'Karivepaku Podi', 'te': 'కరివేపాకు పొడి'},
    'Palli Podi': {'en': 'Palli Podi', 'te': 'పల్లి పొడి'},
    'Kura Podi': {'en': 'Kura Podi', 'te': 'కూర పొడి'},
    'Nuvvula Podi': {'en': 'Nuvvula Podi', 'te': 'నువ్వుల పొడి'},
    'Rasam Powder': {'en': 'Rasam Powder', 'te': 'రసం పొడి'},
    'Sambar Powder': {'en': 'Sambar Powder', 'te': 'సాంబార్ పొడి'},
    
    # Aritaaku - Snacks
    'Mirchi Bajji': {'en': 'Mirchi Bajji', 'te': 'మిర్చి బజ్జి'},
    'Aloo Bajji': {'en': 'Aloo Bajji', 'te': 'ఉర్లగడ్డ బజ్జి'},
    'Aritikay Bajji': {'en': 'Aritikay Bajji', 'te': 'అరితకాయ బజ్జి'},
    'Beerakaya Bajji': {'en': 'Beerakaya Bajji', 'te': 'బీరకాయ బజ్జి'},
    'Onion Bajji': {'en': 'Onion Bajji', 'te': 'ఉల్లిపాయ బజ్జి'},
    'Masala Vada': {'en': 'Masala Vada', 'te': 'మసాల వడ'},
    'Sabudana Vada': {'en': 'Sabudana Vada', 'te': 'సబుదానా వడ'},
    'Sorakaya Garelu': {'en': 'Sorakaya Garelu', 'te': 'సొరకాయ గరెలు'},
    'Kanda Vada': {'en': 'Kanda Vada', 'te': 'కంద వడ'},
    'Onion Pakodi': {'en': 'Onion Pakodi', 'te': 'ఉల్లిపాయ పకోడి'},
    
    # Curries
    'Kanda Bacchali': {'en': 'Kanda Bacchali', 'te': 'కంద బచ్చలి'},
    'Gutti Vankaya - Podi koora': {'en': 'Gutti Vankaya - Podi koora', 'te': 'గుట్టి వంకాయ - పొడి కూర'},
    'Vankaya Ulli Kaaram': {'en': 'Vankaya Ulli Kaaram', 'te': 'వంకాయ ఉల్లి కారం'},
    'Vankaya Allam Pacchimirchi': {'en': 'Vankaya Allam Pacchimirchi', 'te': 'వంకాయ అల్లం పచ్చిమిర్చి'},
    'Vankaya Kaaram Petti': {'en': 'Vankaya Kaaram Petti', 'te': 'వంకాయ కారం పెట్టి'},
    'Chamadumpa fry': {'en': 'Chamadumpa fry', 'te': 'చమడుంప వేపుడు'},
    'Bangaladumpa Fry': {'en': 'Bangaladumpa Fry', 'te': 'బంగాళదుంప వేపుడు'},
    'Vankaya Bangaladumpa Curry': {'en': 'Vankaya Bangaladumpa Curry', 'te': 'వంకాయ బంగాళదుంప కూర'},
    'Aritikaya Mudda Koora': {'en': 'Aritikaya Mudda Koora', 'te': 'అరితకాయ ముద్ద కూర'},
    'Aritikaya Fry': {'en': 'Aritikaya Fry', 'te': 'అరితకాయ వేపుడు'},
    'Bendakaya Pakodi': {'en': 'Bendakaya Pakodi', 'te': 'బెండకాయ పకోడి'},
    'Bendakaya Palli Fry': {'en': 'Bendakaya Palli Fry', 'te': 'బెండకాయ పల్లి వేపుడు'},
    'Bendakaya Kobbari Fry': {'en': 'Bendakaya Kobbari Fry', 'te': 'బెండకాయ కొబ్బరి వేపుడు'},
    'Dondakaya Kobbari Fry': {'en': 'Dondakaya Kobbari Fry', 'te': 'దొండకాయ కొబ్బరి వేపుడు'},
    'Mulakkada Tomato Cashew Curry': {'en': 'Mulakkada Tomato Cashew Curry', 'te': 'ములక్కద టమాట జీడిపప్పు కూర'},
    'Raw Mango Cashew Curry': {'en': 'Raw Mango Cashew Curry', 'te': 'కాచి మామిడి జీడిపప్పు కూర'},
    'Bagara Baingan': {'en': 'Bagara Baingan', 'te': 'బాగర బైంగన్'},
    
    # Dal
    'Tomato Pappu': {'en': 'Tomato Pappu', 'te': 'టమాట పప్పు'},
    'Akukoora Pappu': {'en': 'Akukoora Pappu', 'te': 'ఆకుకూర పప్పు'},
    'Mango Pappu': {'en': 'Mango Pappu', 'te': 'మామిడి పప్పు'},
    'Dosakaya Pappu': {'en': 'Dosakaya Pappu', 'te': 'దోసకాయ పప్పు'},
    'Nimmakaya Pappu': {'en': 'Nimmakaya Pappu', 'te': 'నిమ్మకాయ పప్పు'},
    
    # Roti Pacchadi
    'Dosakaya Mukkala Pacchadi': {'en': 'Dosakaya Mukkala Pacchadi', 'te': 'దోసకాయ ముక్కల పచ్చడి'},
    'Kobbari Pacchadi': {'en': 'Kobbari Pacchadi', 'te': 'కొబ్బరి పచ్చడి'},
    'Tomato Pacchadi': {'en': 'Tomato Pacchadi', 'te': 'టమాట పచ్చడి'},
    'Kothimeera Ullipaya Kaaram': {'en': 'Kothimeera Ullipaya Kaaram', 'te': 'కొత్తిమీర ఉల్లిపాయ కారం'},
    'Gongura Pacchadi': {'en': 'Gongura Pacchadi', 'te': 'గోంగూర పచ్చడి'},
    'Karivepaku Pacchadi': {'en': 'Karivepaku Pacchadi', 'te': 'కరివేపాకు పచ్చడి'},
    'Pudina Pacchadi': {'en': 'Pudina Pacchadi', 'te': 'పుదీనా పచ్చడి'},
    'Kobbari Mamidakaya Pacchadi': {'en': 'Kobbari Mamidakaya Pacchadi', 'te': 'కొబ్బరి మామిడకాయ పచ్చడి'},
    'Ulli Kaaram': {'en': 'Ulli Kaaram', 'te': 'ఉల్లి కారం'},
    'Dondakaya Pacchadi': {'en': 'Dondakaya Pacchadi', 'te': 'దొండకాయ పచ్చడి'},
    'Beerakaya Pacchadi': {'en': 'Beerakaya Pacchadi', 'te': 'బీరకాయ పచ్చడి'},
    
    # Curd Varieties
    'Menthi Majjiga': {'en': 'Menthi Majjiga', 'te': 'మెంతి మజ్జిగ'},
    'Kobbari Perugu Pacchadi': {'en': 'Kobbari Perugu Pacchadi', 'te': 'కొబ్బరి పెరుగు పచ్చడి'},
    'Tomato Perugu Pacchadi': {'en': 'Tomato Perugu Pacchadi', 'te': 'టమాట పెరుగు పచ్చడి'},
    'Vankaya Perugu Pacchadi': {'en': 'Vankaya Perugu Pacchadi', 'te': 'వంకాయ పెరుగు పచ్చడి'},
    
    # Stew
    'Sambar': {'en': 'Sambar', 'te': 'సాంబార్'},
    'Mukkala Pulusu': {'en': 'Mukkala Pulusu', 'te': 'ముక్కల పులుసు'},
    'Pacchi Pulusu': {'en': 'Pacchi Pulusu', 'te': 'పచ్చి పులుసు'},
    'Gummadikaya Pulusu': {'en': 'Gummadikaya Pulusu', 'te': 'గుమ్మడికాయ పులుసు'},
    'Tomato Rasam': {'en': 'Tomato Rasam', 'te': 'టమాట రసం'},
    'Pappu Charu': {'en': 'Pappu Charu', 'te': 'పప్పు చారు'},
    'Majjiga Pulusu': {'en': 'Majjiga Pulusu', 'te': 'మజ్జిగ పులుసు'},
    
    # Desserts
    'Gulab jamun': {'en': 'Gulab jamun', 'te': 'గులాబ్ జామూన్'},
    'Bread Halwa': {'en': 'Bread Halwa', 'te': 'బ్రెడ్ హల్వా'},
    'Carrot Halwa': {'en': 'Carrot Halwa', 'te': 'క్యారెట్ హల్వా'},
    'Semiya Saggubiyam Payasam': {'en': 'Semiya Saggubiyam Payasam', 'te': 'సేమియ సగ్గుబియం పాయసం'},
    'Paramannam': {'en': 'Paramannam', 'te': 'పరమాన్నం'},
    'Sweet Pongal': {'en': 'Sweet Pongal', 'te': 'మిఠాయి పొంగళ్'},
}

def get_menu_translations_js(sheet_name):
    """Generate JavaScript object for menu translations"""
    df = pd.read_excel(xls, sheet_name=sheet_name)
    
    # Build category translations
    categories = OrderedDict()
    for _, row in df.iterrows():
        category = str(row['Category']).strip() if pd.notna(row['Category']) else ''
        if category and category not in categories:
            categories[category] = []
    
    # Build translations object
    cat_translations = {}
    item_translations = {}
    
    for category in categories.keys():
        cat_key = create_category_key(category)
        # Use translation if available, otherwise use original
        if cat_key in CATEGORY_TRANSLATIONS:
            cat_translations[cat_key] = CATEGORY_TRANSLATIONS[cat_key]
        else:
            cat_translations[cat_key] = {'en': category, 'te': category}
    
    # Translation mappings for common terms
    term_translations = {
        'Rice': 'అన్నం', 'Curry': 'కూర', 'Fried': 'వేయించిన', 'Butter': 'వెన్న',
        'Garlic': 'వెల్లుల్లి', 'Tomato': 'టమాట', 'Potato': 'ఉర్లగడ్డ', 'Mixed Veg': 'మిశ్రమ కూరగాయలు',
        'Combo': 'కాంబో', 'Bowls': 'బౌల్స్', 'Panner': 'పనీర్', 'Dal': 'పప్పు',
        'Pickles': 'ఊరగాయలు', 'Powder': 'పొడి', 'Powders': 'పొడులు', 'Snacks': 'చిరుతిండిపదార్థాలు',
        'Desserts': 'మిఠాయిలు', 'Stew': 'స్టూ', 'Varieties': 'రకాలు'
    }
    
    # Add all items - generate Telugu translation
    for _, row in df.iterrows():
        dish_name = str(row['Dish Name']).strip() if pd.notna(row['Dish Name']) else ''
        if dish_name:
            # Try to find translation (check both with and without exact match)
            translation_found = False
            if dish_name in ITEM_TRANSLATIONS:
                item_translations[dish_name] = ITEM_TRANSLATIONS[dish_name]
                translation_found = True
            else:
                # Try to find by stripping (for items with trailing spaces in dict)
                for key, value in ITEM_TRANSLATIONS.items():
                    if key.strip() == dish_name:
                        item_translations[dish_name] = value
                        translation_found = True
                        break
            
            if not translation_found:
                # For items without translation, keep original (many already have Telugu terms)
                item_translations[dish_name] = {'en': dish_name, 'te': dish_name}
    
    # Generate JavaScript object
    import json
    translations_obj = {
        'categories': cat_translations,
        'items': item_translations
    }
    return json.dumps(translations_obj, ensure_ascii=False, indent=16)

def generate_menu_page(sheet_name, page_info):
    """Generate HTML for a menu page"""
    df = pd.read_excel(xls, sheet_name=sheet_name)
    
    # Group by category, preserving order as they appear in Excel
    categories = OrderedDict()
    for _, row in df.iterrows():
        category = str(row['Category']).strip() if pd.notna(row['Category']) else 'Uncategorized'
        dish_name = row['Dish Name'] if pd.notna(row['Dish Name']) else ''
        if dish_name:
            if category not in categories:
                categories[category] = []
            categories[category].append(dish_name)
    
    # Generate accordion HTML (preserving Excel order)
    accordion_html = ""
    for category, items in categories.items():
        category_id = category.lower().replace(' ', '-').replace('&', 'and').replace('/', '-')
        category_key = create_category_key(category)
        items_html = "\n".join([
            f'<div class="menu-item" data-i18n-item="{escape_html(item)}">{escape_html(item)}</div>' 
            for item in items
        ])
        accordion_html += f'''
        <div class="accordion-item" data-category="{escape_html(category)}" data-i18n-category="{category_key}">
            <button class="accordion-header" onclick="toggleAccordion('{category_id}')">
                <span class="accordion-title">{escape_html(category)}</span>
                <span class="accordion-icon" id="icon-{category_id}">▼</span>
            </button>
            <div class="accordion-content" id="content-{category_id}">
                {items_html}
            </div>
        </div>
        '''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>{page_info['title']} - Menu</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #8B3A3A 0%, #7B2D2D 50%, #8B0000 100%);
            background-attachment: fixed;
            min-height: 100vh;
            padding-bottom: 2rem;
            -webkit-text-size-adjust: 100%;
            -webkit-tap-highlight-color: rgba(0,0,0,0.1);
        }}
        
        .header {{
            background: rgba(139, 0, 0, 0.95);
            box-shadow: 0 3px 15px rgba(0,0,0,0.3);
            padding: 0.9rem 0;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(10px);
        }}
        
        .nav-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
        }}
        
        .lang-switcher {{
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }}
        
        .menu-toggle {{
            display: none;
            background: transparent;
            border: 2px solid #FFEAA7;
            border-radius: 6px;
            width: 44px;
            height: 44px;
            cursor: pointer;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 5px;
            padding: 0;
            transition: all 0.3s ease;
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
        }}
        
        .menu-toggle:hover {{
            background: rgba(255, 234, 167, 0.2);
            border-color: #FFD700;
        }}
        
        .menu-toggle span {{
            display: block;
            width: 24px;
            height: 3px;
            background: #FFEAA7;
            border-radius: 2px;
            transition: all 0.3s ease;
        }}
        
        .menu-toggle.active span:nth-child(1) {{
            transform: rotate(45deg) translate(7px, 7px);
        }}
        
        .menu-toggle.active span:nth-child(2) {{
            opacity: 0;
        }}
        
        .menu-toggle.active span:nth-child(3) {{
            transform: rotate(-45deg) translate(7px, -7px);
        }}
        
        .side-nav-overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 998;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .side-nav-overlay.active {{
            display: block;
            opacity: 1;
        }}
        
        .side-nav {{
            position: fixed;
            top: 0;
            left: -280px;
            width: 280px;
            height: 100%;
            background: linear-gradient(135deg, #8B3A3A 0%, #7B2D2D 50%, #8B0000 100%);
            box-shadow: 4px 0 20px rgba(0,0,0,0.5);
            z-index: 999;
            transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            overflow-y: auto;
            padding-top: 1rem;
        }}
        
        .side-nav.active {{
            left: 0;
        }}
        
        .side-nav-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .side-nav-item {{
            border-bottom: 1px solid rgba(255, 234, 167, 0.1);
        }}
        
        .side-nav-item a {{
            display: block;
            padding: 1rem 1.5rem;
            color: #FFEAA7;
            text-decoration: none;
            font-weight: 500;
            font-size: 1rem;
            transition: all 0.25s ease;
            touch-action: manipulation;
        }}
        
        .side-nav-item a:hover {{
            background: rgba(218, 165, 32, 0.3);
            color: #FFD700;
            padding-left: 2rem;
        }}
        
        .side-nav-item a.active {{
            background: #DAA520;
            color: #8B0000;
            font-weight: 600;
        }}
        
        .lang-btn {{
            background: rgba(255, 255, 255, 0.2);
            border: 1.5px solid #FFEAA7;
            color: #FFEAA7;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.25s ease;
            touch-action: manipulation;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .lang-btn:hover {{
            background: rgba(255, 234, 167, 0.3);
            border-color: #FFD700;
        }}
        
        .nav-list {{
            list-style: none;
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
            flex: 1;
        }}
        
        .nav-item a {{
            text-decoration: none;
            color: #FFEAA7;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            transition: all 0.25s ease;
            font-size: 0.95rem;
        }}
        
        .nav-item a:hover {{
            background: rgba(218, 165, 32, 0.3);
            color: #FFD700;
            transform: translateY(-1px);
        }}
        
        .nav-item a.active {{
            background: #DAA520;
            color: #8B0000;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(218, 165, 32, 0.4);
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 1rem;
        }}
        
        h1 {{
            text-align: center;
            color: #FFEAA7;
            margin-bottom: 1.25rem;
            font-size: 2rem;
            font-weight: 700;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.4);
            letter-spacing: -0.5px;
        }}
        
        .search-box {{
            width: 100%;
            padding: 0.85rem 1rem;
            font-size: 0.95rem;
            border: 2px solid #DAA520;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
            background: #FFF8DC;
            color: #5C3A00;
            box-shadow: 0 3px 8px rgba(0,0,0,0.2);
        }}
        
        .search-box::placeholder {{
            color: #8B7355;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: #FFD700;
            box-shadow: 0 4px 12px rgba(218, 165, 32, 0.4);
            transform: translateY(-1px);
        }}
        
        .accordion-item {{
            background: linear-gradient(135deg, #FFF8DC 0%, #FFEAA7 100%);
            border-radius: 10px;
            margin-bottom: 0.75rem;
            box-shadow: 0 3px 12px rgba(0,0,0,0.25);
            overflow: hidden;
            border: 1.5px solid #DAA520;
            transition: box-shadow 0.3s ease;
        }}
        
        .accordion-item:hover {{
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}
        
        .accordion-header {{
            width: 100%;
            padding: 1rem 1.25rem;
            background: linear-gradient(135deg, #FFEAA7 0%, #FFD700 100%);
            border: none;
            text-align: left;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 1rem;
            font-weight: 600;
            color: #8B0000;
            transition: all 0.25s ease;
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
        }}
        
        .accordion-header:hover {{
            background: linear-gradient(135deg, #FFD700 0%, #FFEAA7 100%);
        }}
        
        .accordion-title {{
            flex: 1;
            letter-spacing: -0.2px;
        }}
        
        .accordion-icon {{
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-size: 0.85rem;
            color: #8B0000;
        }}
        
        .accordion-item.active .accordion-icon {{
            transform: rotate(180deg);
        }}
        
        .accordion-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            background: #FFF8DC;
        }}
        
        .accordion-item.active .accordion-content {{
            max-height: 5000px;
            transition: max-height 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .menu-item {{
            padding: 0.7rem 1.25rem;
            border-bottom: 1px solid rgba(218, 165, 32, 0.25);
            color: #5C3A00;
            font-size: 0.95rem;
            transition: background-color 0.2s ease;
        }}
        
        .menu-item:hover {{
            background-color: rgba(255, 248, 220, 0.6);
        }}
        
        .menu-item:last-child {{
            border-bottom: none;
        }}
        
        .no-results {{
            text-align: center;
            padding: 2rem;
            color: #FFEAA7;
            font-size: 1rem;
            background: rgba(139, 0, 0, 0.3);
            border-radius: 10px;
            border: 2px solid #DAA520;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 0.5rem 0 1.5rem;
            }}
            
            .container {{
                padding: 0 0.75rem;
            }}
            
            .header {{
                padding: 0.75rem 0;
                margin-bottom: 1rem;
            }}
            
            .nav-container {{
                padding: 0 0.75rem;
                flex-direction: row;
                gap: 0.75rem;
            }}
            
            .menu-toggle {{
                display: flex;
            }}
            
            .nav-list {{
                display: none;
            }}
            
            .lang-btn {{
                padding: 0.35rem 0.7rem;
                font-size: 0.8rem;
            }}
            
            h1 {{
                font-size: 1.6rem;
                margin-bottom: 1rem;
                line-height: 1.2;
            }}
            
            .search-box {{
                padding: 0.75rem 0.9rem;
                font-size: 16px;
                margin-bottom: 1rem;
                border-width: 2px;
                min-height: 44px;
            }}
            
            .accordion-header {{
                padding: 0.85rem 1rem;
                font-size: 0.95rem;
                min-height: 48px;
            }}
            
            .accordion-item {{
                margin-bottom: 0.6rem;
                border-width: 1.5px;
            }}
            
            .menu-item {{
                padding: 0.65rem 1rem;
                font-size: 0.9rem;
                line-height: 1.5;
            }}
            
            .no-results {{
                padding: 1.5rem;
                font-size: 0.95rem;
            }}
        }}
        
        @media (max-width: 480px) {{
            body {{
                padding: 0.25rem 0 1.25rem;
            }}
            
            .container {{
                padding: 0 0.5rem;
            }}
            
            .header {{
                padding: 0.6rem 0;
                margin-bottom: 0.85rem;
            }}
            
            .nav-container {{
                padding: 0 0.5rem;
            }}
            
            .menu-toggle {{
                width: 40px;
                height: 40px;
            }}
            
            .menu-toggle span {{
                width: 20px;
            }}
            
            .side-nav {{
                width: 260px;
                left: -260px;
            }}
            
            h1 {{
                font-size: 1.4rem;
                margin-bottom: 0.85rem;
            }}
                font-size: 0.8rem;
                flex: 1;
                text-align: center;
                justify-content: center;
            }}
            
            .search-box {{
                padding: 0.7rem 0.85rem;
                font-size: 16px;
                margin-bottom: 0.9rem;
            }}
            
            .accordion-header {{
                padding: 0.75rem 0.9rem;
                font-size: 0.9rem;
            }}
            
            .accordion-item {{
                margin-bottom: 0.5rem;
            }}
            
            .menu-item {{
                padding: 0.6rem 0.9rem;
                font-size: 0.875rem;
            }}
        }}
        
        .whatsapp-float {{
            position: fixed;
            width: 60px;
            height: 60px;
            bottom: 25px;
            right: 25px;
            background: #25D366;
            color: white;
            border-radius: 50%;
            text-align: center;
            font-size: 30px;
            box-shadow: 0 4px 15px rgba(37, 211, 102, 0.5);
            z-index: 1000;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
        }}
        
        .whatsapp-float:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(37, 211, 102, 0.6);
            background: #20BA5A;
        }}
        
        .whatsapp-float svg {{
            width: 35px;
            height: 35px;
            fill: white;
        }}
        
        @media (max-width: 768px) {{
            .whatsapp-float {{
                width: 56px;
                height: 56px;
                bottom: 18px;
                right: 18px;
                font-size: 28px;
                box-shadow: 0 3px 12px rgba(37, 211, 102, 0.45);
            }}
            
            .whatsapp-float:active {{
                transform: scale(0.95);
            }}
            
            .whatsapp-float svg {{
                width: 32px;
                height: 32px;
            }}
        }}
        
        @media (max-width: 480px) {{
            .whatsapp-float {{
                width: 52px;
                height: 52px;
                bottom: 15px;
                right: 15px;
            }}
            
            .whatsapp-float svg {{
                width: 30px;
                height: 30px;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav-container">
            <button class="menu-toggle" id="menuToggle" aria-label="Toggle menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <div class="lang-switcher" style="display: none;">
                <button class="lang-btn" id="langBtnEn" data-lang="en" onclick="switchLanguage('en')" style="display: none;">EN</button>
                <button class="lang-btn" id="langBtnTe" data-lang="te" onclick="switchLanguage('te')" style="display: none;">తెలుగు</button>
            </div>
            <ul class="nav-list">
                <li class="nav-item"><a href="index.html" data-i18n="nav.home">Home</a></li>
                <li class="nav-item"><a href="agrahara-ruchulu.html"{' class="active"' if page_info['url'] == 'agrahara-ruchulu.html' else ''} data-i18n="nav.agrahara">Agrahara Ruchulu</a></li>
                <li class="nav-item"><a href="guntur-kaaram.html"{' class="active"' if page_info['url'] == 'guntur-kaaram.html' else ''} data-i18n="nav.guntur">Guntur Kaaram</a></li>
                <li class="nav-item"><a href="aritaaku.html"{' class="active"' if page_info['url'] == 'aritaaku.html' else ''} data-i18n="nav.aritaaku">Aritaaku</a></li>
            </ul>
        </nav>
    </header>
    
    <div class="side-nav-overlay" id="sideNavOverlay"></div>
    <nav class="side-nav" id="sideNav">
        <ul class="side-nav-list">
            <li class="side-nav-item"><a href="index.html" data-i18n="nav.home">Home</a></li>
            <li class="side-nav-item"><a href="agrahara-ruchulu.html"{' class="active"' if page_info['url'] == 'agrahara-ruchulu.html' else ''} data-i18n="nav.agrahara">Agrahara Ruchulu</a></li>
            <li class="side-nav-item"><a href="guntur-kaaram.html"{' class="active"' if page_info['url'] == 'guntur-kaaram.html' else ''} data-i18n="nav.guntur">Guntur Kaaram</a></li>
            <li class="side-nav-item"><a href="aritaaku.html"{' class="active"' if page_info['url'] == 'aritaaku.html' else ''} data-i18n="nav.aritaaku">Aritaaku</a></li>
        </ul>
    </nav>
    
    <div class="container">
        <h1 data-i18n="page.title.{page_info['url'].replace('.html', '').replace('-', '_')}">{page_info['title']}</h1>
        
        <input type="text" class="search-box" id="searchBox" data-i18n-placeholder="search.placeholder" placeholder="Search categories and items...">
        
        <div id="accordionContainer">
            {accordion_html}
        </div>
        
        <div id="noResults" class="no-results" style="display: none;" data-i18n="search.noResults">
            No items found matching your search.
        </div>
    </div>
    
    <script>
        // Translation data
        const translations = {{
            en: {{
                nav: {{
                    home: "Home",
                    agrahara: "Agrahara Ruchulu",
                    guntur: "Guntur Kaaram",
                    aritaaku: "Aritaaku"
                }},
                page: {{
                    title: {{
                        agrahara_ruchulu: "Agrahara Ruchulu",
                        guntur_kaaram: "Guntur Kaaram",
                        aritaaku: "Aritaaku"
                    }}
                }},
                search: {{
                    placeholder: "Search categories and items...",
                    noResults: "No items found matching your search."
                }}
            }},
            te: {{
                nav: {{
                    home: "హోమ్",
                    agrahara: "అగ్రహార రుచులు",
                    guntur: "గుంటూర్ కారం",
                    aritaaku: "అరితాకు"
                }},
                page: {{
                    title: {{
                        agrahara_ruchulu: "అగ్రహార రుచులు",
                        guntur_kaaram: "గుంటూర్ కారం",
                        aritaaku: "అరితాకు"
                    }}
                }},
                search: {{
                    placeholder: "వర్గాలు మరియు అంశాలను శోధించండి...",
                    noResults: "మీ శోధనకు సరిపడిన అంశాలు ఏవీ కనుగొనబడలేదు."
                }}
            }}
        }};
        
        // Get current language from localStorage or default to English
        let currentLang = localStorage.getItem('language') || 'en';
        
        // Initialize language on page load
        function initLanguage() {{
            updateLanguageButton();
            updatePageLanguage();
        }}
        
        // Update which language button is visible
        function updateLanguageButton() {{
            const btnEn = document.getElementById('langBtnEn');
            const btnTe = document.getElementById('langBtnTe');
            
            if (currentLang === 'en') {{
                // Show Telugu button, hide EN button
                if (btnEn) btnEn.style.display = 'none';
                if (btnTe) btnTe.style.display = 'flex';
            }} else {{
                // Show EN button, hide Telugu button
                if (btnEn) btnEn.style.display = 'flex';
                if (btnTe) btnTe.style.display = 'none';
            }}
        }}
        
        // Switch language
        function switchLanguage(lang) {{
            currentLang = lang;
            localStorage.setItem('language', lang);
            updateLanguageButton();
            updatePageLanguage();
        }}
        
        // Menu item translations (generated from Excel data)
        const menuTranslationsData = {get_menu_translations_js(sheet_name)};
        
        // Update all translatable elements
        function updatePageLanguage() {{
            const langData = translations[currentLang];
            
            // Update elements with data-i18n attribute
            document.querySelectorAll('[data-i18n]').forEach(el => {{
                const key = el.dataset.i18n;
                const keys = key.split('.');
                let value = langData;
                for (let k of keys) {{
                    value = value[k];
                }}
                if (value) el.textContent = value;
            }});
            
            // Update placeholders
            document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {{
                const key = el.dataset.i18nPlaceholder;
                const keys = key.split('.');
                let value = langData;
                for (let k of keys) {{
                    value = value[k];
                }}
                if (value) el.placeholder = value;
            }});
            
            // Update menu categories
            document.querySelectorAll('[data-i18n-category]').forEach(el => {{
                const catKey = el.dataset.i18nCategory;
                const catTrans = menuTranslationsData.categories[catKey];
                if (catTrans) {{
                    const translated = catTrans[currentLang] || el.dataset.category;
                    const titleEl = el.querySelector('.accordion-title');
                    if (titleEl) {{
                        titleEl.textContent = translated;
                    }}
                }}
            }});
            
            // Update menu items
            document.querySelectorAll('[data-i18n-item]').forEach(el => {{
                const itemKey = el.dataset.i18nItem;
                const itemTrans = menuTranslationsData.items[itemKey];
                if (itemTrans) {{
                    const translated = itemTrans[currentLang] || itemKey;
                    el.textContent = translated;
                }} else {{
                    el.textContent = itemKey;
                }}
            }});
        }}
        
        // Initialize on page load
        initLanguage();
        
        // Side navigation toggle
        const menuToggle = document.getElementById('menuToggle');
        const sideNav = document.getElementById('sideNav');
        const sideNavOverlay = document.getElementById('sideNavOverlay');
        
        function toggleSideNav() {{
            menuToggle.classList.toggle('active');
            sideNav.classList.toggle('active');
            sideNavOverlay.classList.toggle('active');
            document.body.style.overflow = sideNav.classList.contains('active') ? 'hidden' : '';
        }}
        
        function closeSideNav() {{
            menuToggle.classList.remove('active');
            sideNav.classList.remove('active');
            sideNavOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }}
        
        if (menuToggle) {{
            menuToggle.addEventListener('click', toggleSideNav);
        }}
        
        if (sideNavOverlay) {{
            sideNavOverlay.addEventListener('click', closeSideNav);
        }}
        
        // Close side nav when clicking on a link
        const sideNavLinks = document.querySelectorAll('.side-nav-item a');
        sideNavLinks.forEach(link => {{
            link.addEventListener('click', () => {{
                setTimeout(closeSideNav, 100);
            }});
        }});
        
        function toggleAccordion(categoryId) {{
            const item = document.querySelector(`#content-${{categoryId}}`).closest('.accordion-item');
            const isActive = item.classList.contains('active');
            
            if (isActive) {{
                item.classList.remove('active');
            }} else {{
                item.classList.add('active');
            }}
        }}
        
        // Search functionality
        const searchBox = document.getElementById('searchBox');
        const accordionContainer = document.getElementById('accordionContainer');
        const noResults = document.getElementById('noResults');
        
        searchBox.addEventListener('input', function(e) {{
            const searchTerm = e.target.value.toLowerCase().trim();
            const accordionItems = accordionContainer.querySelectorAll('.accordion-item');
            let hasResults = false;
            
            if (!searchTerm) {{
                // Reset to default state when search is cleared
                accordionItems.forEach(item => {{
                    item.style.display = '';
                    const menuItems = item.querySelectorAll('.menu-item');
                    menuItems.forEach(menuItem => {{
                        menuItem.style.display = '';
                    }});
                    // Close all accordions by default
                    item.classList.remove('active');
                }});
                noResults.style.display = 'none';
                return;
            }}
            
            accordionItems.forEach(item => {{
                const category = item.getAttribute('data-category').toLowerCase();
                const menuItems = item.querySelectorAll('.menu-item');
                let categoryMatches = category.includes(searchTerm);
                let itemMatches = false;
                
                // Check if any items match
                menuItems.forEach(menuItem => {{
                    const itemText = menuItem.textContent.toLowerCase();
                    if (itemText.includes(searchTerm)) {{
                        itemMatches = true;
                    }}
                }});
                
                // If category matches, show all items; otherwise show only matching items
                menuItems.forEach(menuItem => {{
                    const itemText = menuItem.textContent.toLowerCase();
                    if (categoryMatches || itemText.includes(searchTerm)) {{
                        menuItem.style.display = '';
                    }} else {{
                        menuItem.style.display = 'none';
                    }}
                }});
                
                if (categoryMatches || itemMatches) {{
                    item.style.display = '';
                    item.classList.add('active'); // Expand matching accordions
                    hasResults = true;
                }} else {{
                    item.style.display = 'none';
                }}
            }});
            
            noResults.style.display = !hasResults ? 'block' : 'none';
        }});
    </script>
    
    <a href="https://chat.whatsapp.com/ICyAQQFbLfS6CZi71gNoc3" target="_blank" class="whatsapp-float" aria-label="Join WhatsApp Group">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
        </svg>
    </a>
</body>
</html>
'''
    return html

def generate_index_page():
    """Generate the home page HTML"""
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>Home - Restaurant Menu</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #8B3A3A 0%, #7B2D2D 50%, #8B0000 100%);
            background-attachment: fixed;
            min-height: 100vh;
            padding: 1.5rem 0 2rem;
            -webkit-text-size-adjust: 100%;
            -webkit-tap-highlight-color: rgba(0,0,0,0.1);
        }
        
        .lang-switcher {
            position: fixed;
            top: 1rem;
            right: 1rem;
            display: flex;
            gap: 0.5rem;
            align-items: center;
            z-index: 100;
        }
        
        .lang-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 1.5px solid #FFEAA7;
            color: #FFEAA7;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.25s ease;
            touch-action: manipulation;
            backdrop-filter: blur(10px);
        }
        
        .lang-btn:hover {
            background: rgba(255, 234, 167, 0.3);
            border-color: #FFD700;
        }
        
        .lang-btn {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        h1 {
            text-align: center;
            color: #FFEAA7;
            margin-bottom: 1.5rem;
            font-size: 2.25rem;
            font-weight: 700;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.4);
            letter-spacing: -0.5px;
        }
        
        .cards-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-top: 1rem;
        }
        
        .menu-card {
            background: linear-gradient(135deg, #FFF8DC 0%, #FFEAA7 100%);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 6px 20px rgba(0,0,0,0.35);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
            border: 2px solid #DAA520;
            position: relative;
            overflow: hidden;
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
        }
        
        .menu-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #8B0000, #DAA520, #8B0000);
        }
        
        .menu-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.45);
            border-color: #FFD700;
        }
        
        .menu-card-logo {
            width: 140px;
            height: 140px;
            margin: 0 auto 1rem;
            border-radius: 50%;
            border: 3px solid #DAA520;
            box-shadow: 0 3px 12px rgba(0,0,0,0.25);
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            transition: transform 0.3s ease;
        }
        
        .menu-card:hover .menu-card-logo {
            transform: scale(1.05);
        }
        
        .menu-card-logo img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        
        .menu-card h2 {
            color: #8B0000;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
            letter-spacing: -0.3px;
        }
        
        .menu-card p {
            color: #5C3A00;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        
        @media (max-width: 768px) {
            body {
                padding: 0.75rem 0 1.25rem;
            }
            
            .container {
                padding: 0 0.75rem;
            }
            
            .lang-switcher {
                top: 0.75rem;
                right: 0.75rem;
            }
            
            .lang-btn {
                padding: 0.35rem 0.7rem;
                font-size: 0.8rem;
            }
            
            h1 {
                font-size: 1.6rem;
                margin-bottom: 1rem;
                line-height: 1.2;
            }
            
            .cards-container {
                grid-template-columns: 1fr;
                gap: 1rem;
                margin-top: 0.75rem;
            }
            
            .menu-card {
                padding: 1.25rem 1rem;
                border-width: 2px;
            }
            
            .menu-card-logo {
                width: 110px;
                height: 110px;
                margin-bottom: 0.75rem;
                border-width: 2.5px;
            }
            
            .menu-card h2 {
                font-size: 1.25rem;
                margin-bottom: 0.4rem;
            }
            
            .menu-card p {
                font-size: 0.9rem;
                line-height: 1.4;
            }
        }
        
        @media (max-width: 480px) {
            body {
                padding: 0.5rem 0 1rem;
            }
            
            .container {
                padding: 0 0.5rem;
            }
            
            .lang-switcher {
                top: 0.5rem;
                right: 0.5rem;
            }
            
            .lang-btn {
                padding: 0.3rem 0.6rem;
                font-size: 0.75rem;
            }
            
            h1 {
                font-size: 1.4rem;
                margin-bottom: 0.85rem;
            }
            
            .cards-container {
                gap: 0.85rem;
                margin-top: 0.5rem;
            }
            
            .menu-card {
                padding: 1rem 0.85rem;
                border-radius: 14px;
            }
            
            .menu-card-logo {
                width: 100px;
                height: 100px;
                margin-bottom: 0.65rem;
            }
            
            .menu-card h2 {
                font-size: 1.15rem;
                margin-bottom: 0.35rem;
            }
            
            .menu-card p {
                font-size: 0.85rem;
            }
        }
        
        .whatsapp-float {
            position: fixed;
            width: 60px;
            height: 60px;
            bottom: 25px;
            right: 25px;
            background: #25D366;
            color: white;
            border-radius: 50%;
            text-align: center;
            font-size: 30px;
            box-shadow: 0 4px 15px rgba(37, 211, 102, 0.5);
            z-index: 1000;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            touch-action: manipulation;
            -webkit-tap-highlight-color: transparent;
        }
        
        .whatsapp-float:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(37, 211, 102, 0.6);
            background: #20BA5A;
        }
        
        .whatsapp-float svg {
            width: 35px;
            height: 35px;
            fill: white;
        }
        
        @media (max-width: 768px) {
            .whatsapp-float {
                width: 56px;
                height: 56px;
                bottom: 18px;
                right: 18px;
                font-size: 28px;
                box-shadow: 0 3px 12px rgba(37, 211, 102, 0.45);
            }
            
            .whatsapp-float:active {
                transform: scale(0.95);
            }
            
            .whatsapp-float svg {
                width: 32px;
                height: 32px;
            }
        }
        
        @media (max-width: 480px) {
            .whatsapp-float {
                width: 52px;
                height: 52px;
                bottom: 15px;
                right: 15px;
            }
            
            .whatsapp-float svg {
                width: 30px;
                height: 30px;
            }
        }
    </style>
</head>
<body>
    <div class="lang-switcher" style="display: none;">
        <button class="lang-btn" id="langBtnEn" data-lang="en" onclick="switchLanguage('en')" style="display: none;">EN</button>
        <button class="lang-btn" id="langBtnTe" data-lang="te" onclick="switchLanguage('te')" style="display: none;">తెలుగు</button>
    </div>
    
    <div class="container">
        <h1 data-i18n="home.title">Welcome to Our Menu</h1>
        
        <div class="cards-container">
            <a href="agrahara-ruchulu.html" class="menu-card">
                <div class="menu-card-logo">
                    <img src="agrahararuchulu.webp" alt="Agrahara Ruchulu Logo">
                </div>
                <h2 data-i18n="card.agrahara.title">Agrahara Ruchulu</h2>
                <p data-i18n="card.agrahara.desc">Taste with Tradition<br>Explore our traditional rice bowls and authentic dishes</p>
            </a>
            
            <a href="guntur-kaaram.html" class="menu-card">
                <div class="menu-card-logo">
                    <img src="gunturkaaram.webp" alt="Guntur Kaaram Logo">
                </div>
                <h2 data-i18n="card.guntur.title">Guntur Kaaram</h2>
                <p data-i18n="card.guntur.desc">Pickles & Powders<br>Spicy pickles and flavorful powders</p>
            </a>
            
            <a href="aritaaku.html" class="menu-card">
                <div class="menu-card-logo">
                    <img src="aritaaku.png" alt="Aritaaku Logo">
                </div>
                <h2 data-i18n="card.aritaaku.title">Aritaaku</h2>
                <p data-i18n="card.aritaaku.desc">Premium Veg Catering<br>Delicious snacks and appetizers</p>
            </a>
        </div>
    </div>
    
    <a href="https://chat.whatsapp.com/ICyAQQFbLfS6CZi71gNoc3" target="_blank" class="whatsapp-float" aria-label="Join WhatsApp Group">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
        </svg>
    </a>
    
    <script>
        // Translation data
        const translations = {
            en: {
                home: {
                    title: "Welcome to Our Menu"
                },
                card: {
                    agrahara: {
                        title: "Agrahara Ruchulu",
                        desc: "Taste with Tradition<br>Explore our traditional rice bowls and authentic dishes"
                    },
                    guntur: {
                        title: "Guntur Kaaram",
                        desc: "Pickles & Powders<br>Spicy pickles and flavorful powders"
                    },
                    aritaaku: {
                        title: "Aritaaku",
                        desc: "Premium Veg Catering<br>Delicious snacks and appetizers"
                    }
                }
            },
            te: {
                home: {
                    title: "మా మెనూ కు స్వాగతం"
                },
                card: {
                    agrahara: {
                        title: "అగ్రహార రుచులు",
                        desc: "సంప్రదాయంతో రుచి<br>మా సంప్రదాయ బియ్యం పాత్రలు మరియు ప్రామాణిక వంటకాలను అన్వేషించండి"
                    },
                    guntur: {
                        title: "గుంటూర్ కారం",
                        desc: "ఊరగాయలు & పొడులు<br>కారపు ఊరగాయలు మరియు రుచికరమైన పొడులు"
                    },
                    aritaaku: {
                        title: "అరితాకు",
                        desc: "ప్రీమియం వెజ్ క్యాటరింగ్<br>రుచికరమైన చిరుతిండిపదార్థాలు మరియు ఆపెటైజర్‌లు"
                    }
                }
            }
        };
        
        // Get current language from localStorage or default to English
        let currentLang = localStorage.getItem('language') || 'en';
        
        // Initialize language on page load
        function initLanguage() {
            updateLanguageButton();
            updatePageLanguage();
        }
        
        // Update which language button is visible
        function updateLanguageButton() {
            const btnEn = document.getElementById('langBtnEn');
            const btnTe = document.getElementById('langBtnTe');
            
            if (currentLang === 'en') {
                // Show Telugu button, hide EN button
                if (btnEn) btnEn.style.display = 'none';
                if (btnTe) btnTe.style.display = 'flex';
            } else {
                // Show EN button, hide Telugu button
                if (btnEn) btnEn.style.display = 'flex';
                if (btnTe) btnTe.style.display = 'none';
            }
        }
        
        // Switch language
        function switchLanguage(lang) {
            currentLang = lang;
            localStorage.setItem('language', lang);
            updateLanguageButton();
            updatePageLanguage();
        }
        
        // Update all translatable elements
        function updatePageLanguage() {
            const langData = translations[currentLang];
            
            // Update elements with data-i18n attribute
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.dataset.i18n;
                const keys = key.split('.');
                let value = langData;
                for (let k of keys) {
                    value = value[k];
                }
                if (value) {
                    // Handle HTML content (for <br> tags in descriptions)
                    if (value.includes('<br>')) {
                        el.innerHTML = value;
                    } else {
                        el.textContent = value;
                    }
                }
            });
        }
        
        // Initialize on page load
        initLanguage();
    </script>
</body>
</html>
'''
    return html

# Generate all pages
print("Generating website pages...")

# Generate index page
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(generate_index_page())
print("Generated index.html")

# Generate menu pages
for sheet_name, page_info in pages.items():
    html_content = generate_menu_page(sheet_name, page_info)
    with open(page_info['filename'], 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated {page_info['filename']}")

print("\nWebsite generation complete!")

