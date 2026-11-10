import os
import io
import json
import uuid
import logging
from typing import Dict, Any, Optional, Tuple, List
from PIL import Image
from app.core.config import settings

logger = logging.getLogger(__name__)

# Comprehensive agronomic disease knowledge-base covering all 38 classes (ICAR / standard extension verified)
DISEASE_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    # ---------------- Apple ----------------
    "Apple___Apple_scab": {
        "crop_name": "Apple",
        "disease_name": "Apple Scab (Venturia inaequalis)",
        "description": "Fungal pathogen producing dull olive-green to black velvety spots on leaves and fruit, causing distortion, cracking, and premature leaf drop.",
        "symptoms": [
            "Olive-green to dark brown circular velvety lesions on leaves",
            "Crusty, scabby, or cracked skin lesions on developing apple fruit",
            "Distorted, puckered leaves that turn yellow and drop prematurely",
            "Severely affected fruit stunted or dropped prior to maturity"
        ],
        "treatment_recommendations": [
            "Apply protective fungicide Captan 50% WP @ 2.5 g/L or Mancozeb 75% WP @ 2 g/L at green tip stage",
            "Spray systemic Difenoconazole 25% EC @ 0.5 mL/L or Myclobutanil during active spore discharge",
            "Rake and shred or compost all fallen orchard leaves in autumn to disrupt overwintering pseudothecia",
            "Ensure open pruning canopy for rapid sun drying after morning dew"
        ],
        "preventive_measures": [
            "Plant resistant apple varieties (e.g. Prima, Priscilla, Liberty, Honeycrisp)",
            "Prune inner water sprouts and branches to ensure optimum canopy aeration",
            "Spray urea (5%) on leaf litter in late autumn to speed leaf breakdown"
        ],
        "risk_level": "High"
    },
    "Apple___Black_rot": {
        "crop_name": "Apple",
        "disease_name": "Black Rot (Botryosphaeria obtusa)",
        "description": "Destructive fungal disease causing frog-eye leaf spot, branch cankers, and a firm, mummifying black rot on developing and mature apple fruit.",
        "symptoms": [
            "Small purple specks on leaves expanding into circular frog-eye lesions with tan centers",
            "Sunken, reddish-brown bark cankers on limbs that gradually girdle branches",
            "Fruit rot beginning as brown decay spot with alternating darker and lighter concentric rings",
            "Infected fruit shrivels and remains on branches as black, leathery mummies"
        ],
        "treatment_recommendations": [
            "Prune out dead wood, cankered limbs, and fire blight strikes at least 6-8 inches below margin",
            "Apply Thiophanate-methyl or Captan sprays starting at tight cluster through petal fall",
            "Collect and destroy all dried mummy apples clinging to branches or fallen to the ground",
            "Sanitize pruning shears between cuts with 70% isopropyl alcohol"
        ],
        "preventive_measures": [
            "Avoid wounding tree bark during tractor operations and fruit harvesting",
            "Protect branches from sunscald and winter injury using white latex paint on trunks",
            "Maintain balanced tree nutrition; avoid excessive late-season nitrogen"
        ],
        "risk_level": "High"
    },
    "Apple___Cedar_apple_rust": {
        "crop_name": "Apple",
        "disease_name": "Cedar Apple Rust (Gymnosporangium juniperi-virginianae)",
        "description": "Heteroecious rust fungus cycling between Eastern red cedar / juniper and apple trees, causing bright yellow-orange lesions with fungal tube protrusions.",
        "symptoms": [
            "Bright yellow-orange or reddish spots on upper leaf surfaces in early summer",
            "Small black fungal reproductive specks (pycnia) inside orange leaf spots",
            "Finger-like tubular aecia forming on the underside of leaves and fruit",
            "Premature foliage defoliation and scarred or deformed fruit"
        ],
        "treatment_recommendations": [
            "Spray Myclobutanil (Systhane) @ 1 mL/L or Mancozeb from pink-bud stage until 30 days after petal fall",
            "Apply Trifloxystrobin or Propiconazole on high-risk infection alert windows",
            "Inspect perimeter and remove galls on nearby red cedar / juniper trees before spring rains",
            "Maintain protective spray barrier during wet spring periods when cedar galls form gelatinous horns"
        ],
        "preventive_measures": [
            "Plant rust-resistant apple cultivars such as Freedom, Liberty, or Enterprise",
            "Maintain a buffer zone of at least 500-1000 feet free from Eastern red cedar trees where feasible",
            "Prune gelatinous orange galls from ornamental junipers in early spring before spore release"
        ],
        "risk_level": "Medium"
    },
    "Apple___healthy": {
        "crop_name": "Apple",
        "disease_name": "Healthy Apple Leaf (No Pathogen Detected)",
        "description": "The leaf shows vigorous green pigmentation, uniform cuticle integrity, and zero indications of fungal scabs, rust aecia, or bacterial fire blight.",
        "symptoms": [
            "Uniform green leaf blade with intact margins and healthy petioles",
            "No necrotic frog-eye spots, powdery mildew coatings, or velvety scab patches",
            "Normal vascular vein coloration with no leaf puckering or chlorosis"
        ],
        "treatment_recommendations": [
            "No chemical fungicides or therapeutic bactericides required",
            "Continue seasonal integrated pest management (IPM) monitoring",
            "Maintain balanced irrigation and micronutrient foliar nourishment (Boron, Zinc, Calcium)"
        ],
        "preventive_measures": [
            "Perform routine weekly scouting throughout tree canopy quadrants",
            "Ensure regular orchard floor sanitation and weed clearing",
            "Maintain dormant oil sprays in late winter to suppress overwintering insect vectors"
        ],
        "risk_level": "None"
    },

    # ---------------- Blueberry ----------------
    "Blueberry___healthy": {
        "crop_name": "Blueberry",
        "disease_name": "Healthy Blueberry Leaf (No Pathogen Detected)",
        "description": "The leaf specimen exhibits strong chloroplastic health, normal waxy cuticle development, and complete absence of rust, anthracnose, or botrytis blight.",
        "symptoms": [
            "Smooth, lustrous green leaf surfaces without leaf spot lesions or rust pustules",
            "Firm, upright shoot growth with no stem dieback or cankers",
            "Optimal acidic soil nutrient absorption reflected in clear green foliage"
        ],
        "treatment_recommendations": [
            "No chemical intervention required",
            "Maintain soil pH in the optimal range of 4.5 to 5.2 using elemental sulfur amendments",
            "Supply balanced ammonium-based nitrogen fertilizer in split early-season doses"
        ],
        "preventive_measures": [
            "Apply clean organic pine bark mulch (2-3 inches) to preserve root zone moisture",
            "Drip irrigate using acidified water when required; avoid high bicarbonate overhead water",
            "Scout regularly for blueberry scorch and shock viruses during bloom"
        ],
        "risk_level": "None"
    },

    # ---------------- Cherry ----------------
    "Cherry_(including_sour)___Powdery_mildew": {
        "crop_name": "Cherry",
        "disease_name": "Cherry Powdery Mildew (Podosphaera clandestina)",
        "description": "Airborne fungal disease creating white flour-like powdery mycelial patches on young succulent leaves, causing upward leaf curling and shoot stunting.",
        "symptoms": [
            "Circular to diffuse white powdery fungal patches on young terminal leaves",
            "Leaves curl upward, cup, and become brittle or distorted",
            "Shoot tips stunted or withered, creating a 'witches broom' appearance",
            "Young developing green cherry fruit coated in white powdery mycelium"
        ],
        "treatment_recommendations": [
            "Apply micronized Wettable Sulfur (80% WDG) @ 2.5 g/L at petal fall and shuck fall",
            "Spray Potassium Bicarbonate or Difenoconazole at the earliest sign of mycelial colonization",
            "Alternate with strobilurin fungicides (e.g., Pyraclostrobin) to prevent chemical resistance",
            "Prune infected shoot tips to reduce primary inoculum reservoirs"
        ],
        "preventive_measures": [
            "Ensure proper tree canopy pruning to maximize sunlight penetration and wind movement",
            "Avoid excessive late-season nitrogen applications that provoke vulnerable flush growth",
            "Use drip or micro-sprinkler irrigation rather than overhead sprinkling"
        ],
        "risk_level": "Medium"
    },
    "Cherry_(including_sour)___healthy": {
        "crop_name": "Cherry",
        "disease_name": "Healthy Cherry Leaf (No Pathogen Detected)",
        "description": "The leaf specimen demonstrates healthy deep-green coloration, intact serrated leaf margins, and zero evidence of powdery mildew or shot-hole fungus.",
        "symptoms": [
            "Deep green, well-expanded leaves with characteristic serrated margins",
            "Zero fungal mildew mycelia, chlorotic halos, or necrotic shot-holes",
            "Vigorous shoot growth with healthy petiole attachment"
        ],
        "treatment_recommendations": [
            "No chemical fungicides or treatments required",
            "Maintain regular orchard scouting during high-humidity spring periods",
            "Support fruit development with balanced potassium and calcium foliar sprays"
        ],
        "preventive_measures": [
            "Apply copper sprays at late leaf fall to protect against bacterial canker",
            "Maintain mulch ring around tree dripline to retain moisture and limit root weed competition",
            "Ensure pruning tools are sanitized when shaping young stone fruit branches"
        ],
        "risk_level": "None"
    },

    # ---------------- Corn (Maize) ----------------
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop_name": "Corn (Maize)",
        "disease_name": "Gray Leaf Spot (Cercospora zeae-maydis)",
        "description": "Prevalent foliar fungal disease characterized by rectangular, vein-limited tan or gray lesions that coalesce to cause extensive leaf blighting and lodging.",
        "symptoms": [
            "Small rectangular necrotic spots delimited strictly by parallel leaf veins",
            "Lesions expand into tan-to-gray rectangular stripes (1 to 2 inches long)",
            "Extensive leaf blighting progressing from lower canopy upward during grain filling",
            "Premature stalk lodging due to severe photosynthetic leaf tissue destruction"
        ],
        "treatment_recommendations": [
            "Apply foliar fungicide Azoxystrobin + Difenoconazole @ 1 mL/L or Pyraclostrobin at tassel (VT) stage",
            "Spray Propiconazole 25% EC @ 1 mL/L on susceptible hybrids under high humidity conditions",
            "Plow under or chop surface maize crop residue post-harvest to promote residue decomposition",
            "Avoid continuous corn-on-corn planting cycles"
        ],
        "preventive_measures": [
            "Select high-yielding maize hybrids rated with high Gray Leaf Spot resistance (GLS score 7+)",
            "Implement a 1 to 2-year crop rotation with non-host crops (soybean, sorghum, pulses)",
            "Maintain balanced soil potassium levels to improve stalk strength against lodging"
        ],
        "risk_level": "High"
    },
    "Corn_(maize)___Common_rust_": {
        "crop_name": "Corn (Maize)",
        "disease_name": "Common Rust (Puccinia sorghi)",
        "description": "Wind-borne fungal disease producing prominent cinnamon-brown to dark golden pustules across both upper and lower leaf surfaces.",
        "symptoms": [
            "Small, circular to elongate cinnamon-brown powdery pustules (uredinia) on leaves",
            "Pustules rupture epidermal tissue, releasing rusty orange-brown spores upon touch",
            "Pustules scatter densely across both upper and lower leaf surfaces",
            "Severe infection leads to leaf chlorosis, premature yellowing, and partial necrosis"
        ],
        "treatment_recommendations": [
            "Apply Pyraclostrobin 20% WG or Azoxystrobin @ 1 mL/L if pustules appear before silking",
            "Spray Mancozeb 75% WP @ 2.5 g/L as a protective treatment in seed production fields",
            "Monitor cool, humid weather fronts (60-75°F) with frequent dew which trigger spore release",
            "Fungicide intervention is most economically justified when rust strikes upper ear leaves"
        ],
        "preventive_measures": [
            "Plant maize hybrids containing specific Rp gene resistance against Puccinia sorghi",
            "Sow corn at recommended regional planting dates to avoid late-season airborne rust spore waves",
            "Maintain optimal field drainage and plant spacing"
        ],
        "risk_level": "Medium"
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop_name": "Corn (Maize)",
        "disease_name": "Northern Corn Leaf Blight (Exserohilum turcicum)",
        "description": "Severe fungal foliar pathogen producing large, elliptical 'cigar-shaped' grayish-green lesions that cause extensive canopy burn and yield loss.",
        "symptoms": [
            "Long, elliptical, cigar-shaped grayish-green or tan lesions (1 to 6 inches long)",
            "Lesions form dark olive-black velvety spore mats on underside during damp mornings",
            "Lesions coalesce, causing entire leaves to turn dry, brittle, and scorched",
            "Premature plant death and reduced grain test weight when upper ear leaves are blighted"
        ],
        "treatment_recommendations": [
            "Spray Pyraclostrobin + Fluxapyroxad or Azoxystrobin + Propiconazole at VT/R1 stage",
            "Apply Mancozeb 75% WP @ 2.5 g/L or Chlorothalonil early in disease progression",
            "Perform deep tillage or bury infected corn stubble to speed biological decay",
            "Rotate field out of corn for at least 1-2 seasons in fields with heavy blight history"
        ],
        "preventive_measures": [
            "Select resistant hybrids with Ht1, Ht2, Ht3, or polygenic resistance genes",
            "Maintain balanced fertility (adequate potassium; avoid excessive free nitrogen)",
            "Eliminate volunteer corn plants and grassy alternate hosts around field borders"
        ],
        "risk_level": "High"
    },
    "Corn_(maize)___healthy": {
        "crop_name": "Corn (Maize)",
        "disease_name": "Healthy Corn Foliage (No Pathogen Detected)",
        "description": "The maize leaf blade displays robust deep-green coloration, healthy parallel venation, and no signs of rust pustules, cigar lesions, or fungal blighting.",
        "symptoms": [
            "Broad, deep green leaf blades with sturdy midribs and clean parallel veins",
            "Complete absence of necrotic lesions, powdery rust uredinia, or chlorotic streaking",
            "Vigorous photosynthetic activity supporting active vegetative and reproductive stages"
        ],
        "treatment_recommendations": [
            "No chemical fungicides or treatments needed",
            "Conduct routine scouting throughout knee-high (V6) and tasseling (VT) growth stages",
            "Apply scheduled side-dress nitrogen fertilizer according to soil test recommendations"
        ],
        "preventive_measures": [
            "Ensure regular irrigation scheduling during critical silking and grain filling periods",
            "Scout for fall armyworm and stem borer presence beneath whorl foliage",
            "Practice standard crop rotation after harvest to sustain soil biome health"
        ],
        "risk_level": "None"
    },

    # ---------------- Grape ----------------
    "Grape___Black_rot": {
        "crop_name": "Grape",
        "disease_name": "Grape Black Rot (Guignardia bidwellii)",
        "description": "Devastating fungal disease causing small circular reddish-brown leaf spots with black fruiting pycnidia and shriveling berries into hard black mummies.",
        "symptoms": [
            "Circular reddish-brown spots with dark borders on leaves, containing tiny black specks (pycnidia)",
            "Black elongated cankers on young shoots, petioles, and tendrils",
            "Berries develop soft brown rot spots, then rapidly shrivel into hard, black, wrinkled mummies",
            "Mummified berries remain firmly attached to the cluster rachis"
        ],
        "treatment_recommendations": [
            "Apply Mancozeb 75% WP @ 2 g/L or Captan 50% WP @ 2.5 g/L from bud break to bloom",
            "Spray systemic Myclobutanil @ 1 mL/L or Azoxystrobin @ 1 mL/L immediately pre-bloom and post-bloom",
            "Prune out and destroy all mummified fruit clusters and cankered canes during dormant pruning",
            "Keep vineyard floor free of infected fallen mummies before spring bud swell"
        ],
        "preventive_measures": [
            "Maintain open canopy trellis systems (e.g. VSP or Scott Henry) to allow sunlight and rapid air flow",
            "Direct drip irrigation to root zones rather than wetting foliage with sprinklers",
            "Cultivate soil lightly in early spring to bury overwintering berry mummies"
        ],
        "risk_level": "High"
    },
    "Grape___Esca_(Black_Measles)": {
        "crop_name": "Grape",
        "disease_name": "Esca / Black Measles (Phaeomoniella / Phaeoacremonium complex)",
        "description": "Chronic vascular trunk disease causing dramatic 'tiger-stripe' interveinal leaf scorch, dark spotting on berries ('measles'), and sudden vine apoplexy.",
        "symptoms": [
            "'Tiger-stripe' chlorotic and necrotic patterns between green veins on leaves",
            "Small dark brown to purplish spots ('black measles') speckled across grape berry skin",
            "Dark brown wood vascular striping visible when infected trunks and cordons are cut",
            "Sudden vine apoplexy: total foliage wilting and berry collapse during summer heat spikes"
        ],
        "treatment_recommendations": [
            "Paint all large dormant pruning wounds with wound sealants containing Boric acid or Thiophanate-methyl",
            "Prune vines late in winter dormancy when wound healing occurs more rapidly",
            "Mark severely infected vines and prune them last to prevent tool transmission",
            "Retrain a healthy bottom sucker (water sprout) to regenerate trunk if vine scaffold is diseased"
        ],
        "preventive_measures": [
            "Use certified clean, disease-free nursery rootstocks and scions",
            "Avoid large flush pruning cuts that expose heartwood during wet winter periods",
            "Apply Trichoderma-based biological wound protectants directly to fresh pruning cuts"
        ],
        "risk_level": "Critical"
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop_name": "Grape",
        "disease_name": "Grape Leaf Blight (Pseudocercospora vitis / Isariopsis clavispora)",
        "description": "Foliar fungal pathogen producing irregular angular dark brown necrotic spots that coalesce, causing premature vine defoliation and compromised grape sugar content.",
        "symptoms": [
            "Angular to irregular dark brown lesions with distinct darker reddish borders on leaves",
            "Velvety olive-brown fungal spore tufts developing on the lesion undersides",
            "Coalescence of lesions leading to extensive leaf scorch and early canopy drop",
            "Poor wood maturation and lowered brix (sugar accumulation) in grape bunches"
        ],
        "treatment_recommendations": [
            "Spray Copper Oxychloride 50% WP @ 2.5 g/L or Bordeaux Mixture (1%) at first sign of spots",
            "Apply Mancozeb 75% WP @ 2 g/L or Carbendazim 50% WP @ 1 g/L as a protective foliar spray",
            "Ensure good leaf removal around grape clusters (leaf pulling) for ventilation",
            "Collect and burn fallen vineyard leaf debris after harvest"
        ],
        "preventive_measures": [
            "Select resistant cultivars suited to regional summer rainfall climates",
            "Manage vine vigor by avoiding excessive nitrogen applications",
            "Maintain clean vineyard row middles to reduce relative humidity"
        ],
        "risk_level": "Medium"
    },
    "Grape___healthy": {
        "crop_name": "Grape",
        "disease_name": "Healthy Grapevine Leaf (No Pathogen Detected)",
        "description": "The grapevine foliage shows vibrant chlorophyll distribution, clean lobed margins, strong vein integrity, and complete freedom from fungal mildew or vascular leaf scorch.",
        "symptoms": [
            "Vibrant green, fully expanded lobed grape leaves with intact cuticle",
            "Clean leaf undersides without downy white or powdery gray fungal sporulation",
            "Firm petiole connections and vigorous tendril shoot development"
        ],
        "treatment_recommendations": [
            "No chemical fungicides or treatments required",
            "Continue canopy management (shoot positioning, suckering, and lateral pruning)",
            "Maintain balanced potassium and magnesium nutrition to ensure berry cluster fill"
        ],
        "preventive_measures": [
            "Scout canopy weekly for early downy mildew oil spots or powdery mildew flags",
            "Maintain drip irrigation schedule based on evapo-transpiration (ETc) requirements",
            "Sanitize vineyard mechanical hedging equipment between vineyard blocks"
        ],
        "risk_level": "None"
    },

    # ---------------- Orange / Citrus ----------------
    "Orange___Haunglongbing_(Citrus_greening)": {
        "crop_name": "Orange",
        "disease_name": "Huanglongbing / Citrus Greening (Candidatus Liberibacter asiaticus)",
        "description": "Catastrophic phloem-limited bacterial disease vectored by the Asian Citrus Psyllid, causing asymmetrical blotchy leaf mottle, small lopsided bitter fruit, and tree death.",
        "symptoms": [
            "Asymmetrical 'blotchy mottle' chlorosis across leaf midribs (random yellowing)",
            "Thickened, leathery leaves with raised corky veins ('rabbit ear' upright posture)",
            "Yellow shoots standing out within otherwise green canopies ('yellow dragon')",
            "Small, lopsided, poorly colored fruit with bitter taste and aborted dark seeds"
        ],
        "treatment_recommendations": [
            "Immediately control the Asian Citrus Psyllid vector with systemic Imidacloprid, Thiamethoxam, or Dimethoate",
            "Spray horticultural petroleum mineral oils or Azadirachtin (Neem 10,000 ppm) to deter psyllid egg-laying",
            "Severely diseased trees must be cut at soil line and herbicide-treated to prevent root suckering",
            "Apply foliar nutritional sprays (Zinc, Manganese, Iron, Magnesium, Potassium) to prolong productive life of infected trees"
        ],
        "preventive_measures": [
            "Plant only certified disease-free citrus trees produced under insect-proof screenhouses",
            "Maintain regional psyllid quarantine protocols; never transport uncertified budwood or plant material",
            "Deploy yellow sticky traps throughout citrus orchards to monitor adult psyllid populations"
        ],
        "risk_level": "Critical"
    },

    # ---------------- Peach ----------------
    "Peach___Bacterial_spot": {
        "crop_name": "Peach",
        "disease_name": "Peach Bacterial Spot (Xanthomonas arboricola pv. pruni)",
        "description": "Bacterial pathogen creating small angular purple-brown leaf spots that drop out to leave a 'shot-hole' appearance, deep fruit pitting, and stem cankers.",
        "symptoms": [
            "Small, angular, water-soaked spots on leaves turning dark purple to brown",
            "Centers of leaf spots drop out, producing a distinct 'shot-hole' appearance",
            "Leaves turn yellow and defoliate prematurely, particularly near shoot tips",
            "Sunken, dark circular spots on fruit surface leading to deep cracks and gummy exudate"
        ],
        "treatment_recommendations": [
            "Apply fixed Copper bactericides (e.g. Copper Hydroxide) during dormant and bud swell stages",
            "Spray Oxytetracycline (Mycoshield) @ 1.5 g/L from petal fall through fruit maturation at 7-day intervals",
            "Avoid overhead sprinkler irrigation that splashes bacterial cells onto foliage",
            "Prune during dry sunny weather to limit bacterial spread across fresh wound sites"
        ],
        "preventive_measures": [
            "Select peach cultivars with recognized bacterial spot resistance (e.g. Redhaven, Harrow Diamond)",
            "Plant windbreaks around sandy orchard perimeters to reduce blowing sand leaf abrasion",
            "Maintain moderate tree vigor; avoid excess nitrogen which induces soft, vulnerable tissue"
        ],
        "risk_level": "High"
    },
    "Peach___healthy": {
        "crop_name": "Peach",
        "disease_name": "Healthy Peach Leaf (No Pathogen Detected)",
        "description": "The peach leaf shows vibrant lanceolate morphology, glossy green surface, smooth margins, and complete absence of bacterial shot-holes or leaf curl blisters.",
        "symptoms": [
            "Lustrous, long lanceolate green leaves with intact, smooth margins",
            "No reddish puckered blisters (peach leaf curl) or necrotic shot-holes",
            "Strong shoot elongation with healthy bud development at leaf axils"
        ],
        "treatment_recommendations": [
            "No chemical fungicides or bactericides required",
            "Continue standard stone fruit integrated pest management (IPM)",
            "Maintain adequate soil moisture during summer fruit sizing"
        ],
        "preventive_measures": [
            "Apply dormant copper or chlorothalonil spray before bud swell in late winter to prevent leaf curl",
            "Ensure regular orchard floor sanitation and clean tree dripline weed management",
            "Prune scaffold branches annually in open-vase shape to optimize light penetration"
        ],
        "risk_level": "None"
    },

    # ---------------- Pepper (Bell) ----------------
    "Pepper,_bell___Bacterial_spot": {
        "crop_name": "Pepper (Bell)",
        "disease_name": "Bell Pepper Bacterial Spot (Xanthomonas campestris pv. vesicatoria)",
        "description": "Destructive seed-borne and splash-dispersed bacterial pathogen causing water-soaked angular leaf spots, severe defoliation, and rough wart-like fruit scabs.",
        "symptoms": [
            "Small, circular to irregular water-soaked spots on leaf undersides",
            "Lesions enlarge to 1/8 inch, turning dark brown with yellow chlorotic halos",
            "Extensive lower leaf yellowing and defoliation, exposing fruit to sunscald",
            "Rough, raised, blister-like or wart-like scabs on bell pepper fruit"
        ],
        "treatment_recommendations": [
            "Spray Copper Hydroxide 53.8% DF combined with Mancozeb 75% WP @ 2 g/L on a 7-day schedule",
            "Apply Streptocycline @ 1 g / 10 L water or Kasugamycin during severe bacterial outbreaks",
            "Avoid entering fields or handling pepper plants while foliage is wet from rain or dew",
            "Immediately destroy and bury crop residues after final harvest"
        ],
        "preventive_measures": [
            "Use certified disease-free treated seed (hot-water treatment at 50°C for 25 minutes)",
            "Select bell pepper varieties with multi-race resistance (Xv-1 through Xv-10)",
            "Practice minimum 2 to 3-year crop rotation away from solanaceous plants (tomato, potato, chili)"
        ],
        "risk_level": "High"
    },
    "Pepper,_bell___healthy": {
        "crop_name": "Pepper (Bell)",
        "disease_name": "Healthy Bell Pepper Leaf (No Pathogen Detected)",
        "description": "The pepper foliage exhibits deep-green color, smooth glossy texture, sturdy petiole structure, and complete absence of bacterial spots or viral mosaic mottling.",
        "symptoms": [
            "Dark green, glossy, smooth ovate leaves with clean, intact margins",
            "Zero water-soaked bacterial lesions, necrotic speckling, or yellow mottling",
            "Sturdy upright canopy growth with healthy flowering and fruit set"
        ],
        "treatment_recommendations": [
            "No chemical intervention or pesticide treatments required",
            "Maintain steady drip irrigation to prevent blossom end rot (BER)",
            "Apply balanced NPK fertilizer with calcium and magnesium supplements"
        ],
        "preventive_measures": [
            "Scout weekly for aphids, thrips, and whiteflies to prevent viral vector transmission",
            "Mulch beds with organic straw or reflective plastic mulch to regulate soil moisture",
            "Keep perimeter clear of nightshade weed reservoirs"
        ],
        "risk_level": "None"
    },

    # ---------------- Potato ----------------
    "Potato___Early_blight": {
        "crop_name": "Potato",
        "disease_name": "Potato Early Blight (Alternaria solani)",
        "description": "Common foliar fungal disease creating brown-black concentric target-like rings on older leaves, progressing upward and reducing tuber yield.",
        "symptoms": [
            "Dark brown to black circular lesions displaying distinct concentric rings ('target board')",
            "Yellow halo of chlorosis surrounding older necrotic lesions",
            "Lower mature leaves become dry, papery, and drop prematurely",
            "Tubers develop brown, dry, corky sunken rot lesions beneath skin"
        ],
        "treatment_recommendations": [
            "Spray Mancozeb 75% WP @ 2.5 g/L or Chlorothalonil 75% WP @ 2 g/L at first symptom detection",
            "Rotate with systemic fungicides Azoxystrobin (Amistar) @ 1 mL/L or Difenoconazole",
            "Prune and discard infected lower leaves during early field stage",
            "Switch from overhead sprinkler to furrow or drip irrigation to keep canopy dry"
        ],
        "preventive_measures": [
            "Implement a 3-year crop rotation avoiding tomato, brinjal, and other Solanaceae",
            "Plant certified disease-free seed tubers treated with fungicide prior to planting",
            "Maintain optimal crop nutrition; plants suffering nitrogen or potassium deficiency are most susceptible"
        ],
        "risk_level": "Medium"
    },
    "Potato___Late_blight": {
        "crop_name": "Potato",
        "disease_name": "Potato Late Blight (Phytophthora infestans)",
        "description": "Catastrophic water-mold oomycete causing rapid water-soaked foliage collapse, white fungal mildew under leaves in high humidity, and rotting tubers.",
        "symptoms": [
            "Large, irregular water-soaked spots rapidly expanding into dark brown/black foliage rot",
            "Delicate white cottony mildew growth visible on leaf undersides during moist mornings",
            "Total collapse and blackening of foliage canopy in 3-5 days under cool, humid weather",
            "Purplish-brown dry rot extending into tuber flesh beneath skin, followed by soft bacterial breakdown"
        ],
        "treatment_recommendations": [
            "Immediately spray Metalaxyl 8% + Mancozeb 64% WP (Ridomil MZ) @ 2.5 g/L upon local blight alert trigger",
            "Apply systemic Cymoxanil + Mancozeb or Dimethomorph 50% WP @ 1.5 g/L on 5-7 day cycles",
            "Cut and burn potato haulms (vines) 10-14 days before harvest to prevent tuber contamination",
            "Ensure harvested tubers cure in dry shade before bagging; discard any rot-damaged tubers"
        ],
        "preventive_measures": [
            "Plant certified disease-free seed tubers obtained from accredited seed corporations",
            "Perform proper high hilling / earthing-up to shield tubers under a thick soil barrier",
            "Follow IMD / AgriSaathi weather blight alerts and apply preventive protectants before rainy spells"
        ],
        "risk_level": "Critical"
    },
    "Potato___healthy": {
        "crop_name": "Potato",
        "disease_name": "Healthy Potato Leaf (No Pathogen Detected)",
        "description": "The potato foliage shows strong compound leaf formation, vibrant green coloration, intact veins, and complete freedom from early or late blight pathogens.",
        "symptoms": [
            "Healthy compound leaves with robust green leaflets and smooth margins",
            "No concentric target spots, water-soaked blotches, or white underleaf sporulation",
            "Firm upright stems with vigorous tuber initiation beneath hill"
        ],
        "treatment_recommendations": [
            "No chemical fungicides or interventions needed",
            "Maintain regular field monitoring, especially following rainfall and morning fogs",
            "Provide balanced NPK nutrition (supplement potash during tuber expansion)"
        ],
        "preventive_measures": [
            "Perform timely earthing up to ensure developing tubers are protected from sunlight and spores",
            "Ensure well-drained field conditions with no standing water in furrows",
            "Scout for aphids and Colorado potato beetle larvae"
        ],
        "risk_level": "None"
    },

    # ---------------- Raspberry ----------------
    "Raspberry___healthy": {
        "crop_name": "Raspberry",
        "disease_name": "Healthy Raspberry Leaf (No Pathogen Detected)",
        "description": "The cane leaf displays vigorous palmate compound structure, clean serrated edges, and zero symptoms of spur blight, cane blight, or anthracnose.",
        "symptoms": [
            "Deep green serrated leaflets with characteristic silver-green undersides",
            "Zero purple cane lesions, leaf spots, or powdery mildew coatings",
            "Sturdy primocane and floricane shoot growth supporting active flowering/fruiting"
        ],
        "treatment_recommendations": [
            "No chemical treatments required",
            "Ensure canes are trellised upright to optimize sunlight and airflow",
            "Maintain moderate drip irrigation and organic compost mulch"
        ],
        "preventive_measures": [
            "Prune out spent floricanes immediately post-harvest to reduce fungal disease buildup",
            "Thin out primocanes to 4-6 sturdy canes per foot of row",
            "Keep bramble patch free of perennial weeds and wild bramble reservoirs"
        ],
        "risk_level": "None"
    },

    # ---------------- Soybean ----------------
    "Soybean___healthy": {
        "crop_name": "Soybean",
        "disease_name": "Healthy Soybean Leaf (No Pathogen Detected)",
        "description": "The trifoliate leaf exhibits robust green chloroplastic health, normal pubescence, and complete absence of Asian soybean rust, frogeye leaf spot, or mosaic.",
        "symptoms": [
            "Clean trifoliate green leaves with intact margins and healthy fine pubescence",
            "Zero reddish-brown rust pustules, circular frogeye spots, or vein clearing",
            "Vigorous nodulation and vegetative canopy development"
        ],
        "treatment_recommendations": [
            "No chemical fungicides or insecticides required",
            "Perform routine canopy scouting during reproductive stages (R1 to R5)",
            "Ensure adequate rhizobial seed inoculation during planting"
        ],
        "preventive_measures": [
            "Practice 2-year crop rotation with corn, wheat, or non-legume crops",
            "Ensure proper field drainage to avoid root rot complexes during monsoon season",
            "Scout for defoliating caterpillars and stem fly infestation"
        ],
        "risk_level": "None"
    },

    # ---------------- Squash ----------------
    "Squash___Powdery_mildew": {
        "crop_name": "Squash",
        "disease_name": "Squash Powdery Mildew (Podosphaera xanthii)",
        "description": "Ubiquitous foliar fungal disease forming conspicuous white talcum powder-like mycelial patches on both leaf surfaces, leading to yellowing, defoliation, and fruit sunburn.",
        "symptoms": [
            "White, talcum-powder-like fungal circular spots on leaves and stems",
            "Spots rapidly expand and merge, coating the entire upper and lower leaf blade",
            "Infected leaves turn yellow, then brown, brittle, and wither completely",
            "Defoliation exposes developing squash fruit to sunscald and premature ripening"
        ],
        "treatment_recommendations": [
            "Apply Wettable Sulfur 80% WP @ 2.5 g/L or Potassium Bicarbonate @ 3 g/L at first sign of white spots",
            "Spray Triadimefon 25% WP @ 0.5 g/L or Myclobutanil for systemic curative action",
            "Spray horticultural neem oil (1%) or biological Bacillus amyloliquefaciens preventive biofungicides",
            "Remove and destroy severely affected older leaves to reduce spore dispersal"
        ],
        "preventive_measures": [
            "Plant resistant squash and pumpkin cultivars possessing PM resistance genes",
            "Allow generous spacing between squash hills (4-6 feet) for air circulation",
            "Irrigate squash plants at the root base using drip tape; keep broad leaves dry"
        ],
        "risk_level": "Medium"
    },

    # ---------------- Strawberry ----------------
    "Strawberry___Leaf_scorch": {
        "crop_name": "Strawberry",
        "disease_name": "Strawberry Leaf Scorch (Diplocarpon earlianum)",
        "description": "Fungal pathogen causing numerous small irregular purplish to dark brown spots that lack white centers, causing leaf margins to curl up and look scorched.",
        "symptoms": [
            "Small, irregular purple to dark brown spots scattered over upper leaf surface",
            "Unlike leaf spot, lesions remain dark purple without developing white or grey centers",
            "Spots coalesce, causing tissue between spots to turn reddish-brown or purplish",
            "Leaf margins curl upward and dry out, giving the plant a scorched, fire-burned appearance"
        ],
        "treatment_recommendations": [
            "Spray Captan 50% WP @ 2.5 g/L or Copper Hydroxide @ 2 g/L during spring crown emergence",
            "Apply Azoxystrobin (Amistar) @ 1 mL/L or Pyraclostrobin during active leaf expansion",
            "Mow and destroy old foliage immediately following post-harvest strawberry bed renovation",
            "Improve bed drainage and thin crowded runner plants to improve airflow"
        ],
        "preventive_measures": [
            "Plant certified disease-free strawberry runners on raised plastic-mulched beds",
            "Avoid overhead irrigation; use drip lines under plastic mulch",
            "Rotate strawberry plantings to new ground every 3-4 years"
        ],
        "risk_level": "Medium"
    },
    "Strawberry___healthy": {
        "crop_name": "Strawberry",
        "disease_name": "Healthy Strawberry Leaf (No Pathogen Detected)",
        "description": "The trifoliate strawberry leaf specimen shows bright green coloration, deep serrations, firm petioles, and complete freedom from leaf scorch, blight, or powdery mildew.",
        "symptoms": [
            "Lustrous deep-green trifoliate leaflets with sharp, clean serrations",
            "Zero purple necrotic spotting, angular water-soaking, or white powdery coatings",
            "Sturdy petiole and crown structure with vigorous runner development"
        ],
        "treatment_recommendations": [
            "No chemical fungicides or sprays needed",
            "Continue standard strawberry bed nutrition and trickle irrigation",
            "Supply soluble calcium and potassium to support firm berry formation"
        ],
        "preventive_measures": [
            "Maintain clean straw or plastic mulch beneath fruit clusters to prevent soil-contact rot",
            "Scout regularly for two-spotted spider mites and crown rot symptoms",
            "Sanitize runner clipping tools during bed grooming"
        ],
        "risk_level": "None"
    },

    # ---------------- Tomato ----------------
    "Tomato___Bacterial_spot": {
        "crop_name": "Tomato",
        "disease_name": "Tomato Bacterial Spot (Xanthomonas spp.)",
        "description": "Bacterial pathogen causing small, dark, water-soaked leaf lesions with yellow halos, defoliation, and raised scabby spots on tomato fruit.",
        "symptoms": [
            "Small (less than 1/8 inch), circular, dark brown to black water-soaked leaf spots",
            "Spots frequently surrounded by a distinct yellow chlorotic halo",
            "Severe spotting causes leaflets to yellow, wither, and drop, exposing fruit to sunscald",
            "Fruit develops small, slightly raised, blister-like or scabby brown blemishes"
        ],
        "treatment_recommendations": [
            "Spray Copper Oxychloride 50% WP @ 2.5 g/L combined with Streptocycline @ 1 g / 10 L water",
            "Alternate with Mancozeb 75% WP @ 2 g/L tank-mixed with copper for enhanced bactericidal efficacy",
            "Avoid overhead sprinkler irrigation; always utilize drip or furrow irrigation",
            "Never work in or prune tomato plants while foliage is wet from morning dew or rain"
        ],
        "preventive_measures": [
            "Plant certified pathogen-free seeds treated with hot water or hydrochloric acid",
            "Practice a minimum 2 to 3-year crop rotation avoiding tomato, pepper, and potato",
            "Sanitize stakes, trellises, and harvest crates with a 10% sodium hypochlorite solution"
        ],
        "risk_level": "High"
    },
    "Tomato___Early_blight": {
        "crop_name": "Tomato",
        "disease_name": "Tomato Early Blight (Alternaria solani)",
        "description": "Fungal disease causing brown-black concentric target-like rings on older leaves, progressing upward and leading to premature defoliation and yield loss.",
        "symptoms": [
            "Concentric dark brown rings forming target spots on lower mature foliage",
            "Yellow halo (chlorosis) surrounding older necrotic lesions",
            "Stem cankers near soil level (collar rot) on seedlings and lower stems",
            "Sunken, dark leathery lesions at stem end of tomato fruit"
        ],
        "treatment_recommendations": [
            "Apply Copper Oxychloride 50% WP @ 2.5 g/L or Mancozeb 75% WP @ 2 g/L at first symptom onset",
            "Spray systemic Azoxystrobin (Amistar) @ 1 mL/L or Difenoconazole on 7-10 day rotation",
            "Prune infected bottom leaves during dry weather to enhance air circulation",
            "Employ drip irrigation instead of overhead sprinklers to keep foliage dry"
        ],
        "preventive_measures": [
            "Practice 3-year crop rotation avoiding Solanaceous family crops (potato, brinjal, chili)",
            "Use certified disease-free treated seeds or resistant tomato cultivars",
            "Stake plants and mulch soil with clean organic straw to prevent soil-splash pathogens",
            "Sanitize all pruning tools in 10% bleach solution between plant rows"
        ],
        "risk_level": "High"
    },
    "Tomato___Late_blight": {
        "crop_name": "Tomato",
        "disease_name": "Tomato Late Blight (Phytophthora infestans)",
        "description": "Water-mold pathogen causing rapid water-soaked lesions, white fuzzy sporulation on leaf undersides, and destructive fruit rot in cool, humid conditions.",
        "symptoms": [
            "Pale green, water-soaked irregular spots rapidly enlarging into brown blotches",
            "Delicate white cottony fungal growth on leaf undersides during moist mornings",
            "Dark brown blotchy discoloration and rotting of green and ripe fruit",
            "Rapid total collapse of plant foliage ('blighted' appearance)"
        ],
        "treatment_recommendations": [
            "Immediately spray Metalaxyl 8% + Mancozeb 64% WP (Ridomil MZ) @ 2.5 g/L",
            "Alternate with Dimethomorph 50% WP or Cymoxanil combinations on 5-day intervals",
            "Destroy and bury severely diseased plants away from field immediately",
            "Cease all sprinkler and furrow irrigation to lower localized humidity"
        ],
        "preventive_measures": [
            "Avoid planting near potato fields harboring latent late blight inoculum",
            "Select resistant varieties with Ph-2 and Ph-3 gene resistance",
            "Ensure wide plant spacing for rapid canopy drying after morning dew",
            "Monitor weather forecast alerts for extended cloudy, high-humidity periods"
        ],
        "risk_level": "Critical"
    },
    "Tomato___Leaf_Mold": {
        "crop_name": "Tomato",
        "disease_name": "Tomato Leaf Mold (Passalora fulva / Cladosporium fulvum)",
        "description": "Fungal pathogen prevalent in greenhouse and high-tunnel environments, producing pale green to yellow chlorotic spots on upper leaf surfaces and velvety olive-brown mold beneath.",
        "symptoms": [
            "Pale green to yellowish chlorotic spots with indefinite margins on upper leaf surface",
            "Dense, velvety olive-green to brownish fungal mold growth on leaf undersides",
            "Infected leaves curl, wither, turn reddish-brown, and drop prematurely",
            "Defoliation progresses from bottom leaves upward, significantly lowering yield"
        ],
        "treatment_recommendations": [
            "Spray Copper Hydroxide @ 2 g/L or Chlorothalonil 75% WP @ 2 g/L at first appearance of spots",
            "Apply systemic Difenoconazole @ 0.5 mL/L or Azoxystrobin for curative knockdown",
            "Increase greenhouse ventilation with exhaust fans to reduce relative humidity below 85%",
            "Prune lower suckers and dense foliage to allow horizontal airflow across beds"
        ],
        "preventive_measures": [
            "Plant tomato varieties possessing Cf resistance genes against Passalora fulva",
            "Avoid overhead watering; maintain dry foliage at all times",
            "Sanitize greenhouse structures and tools thoroughly between crop cycles"
        ],
        "risk_level": "Medium"
    },
    "Tomato___Septoria_leaf_spot": {
        "crop_name": "Tomato",
        "disease_name": "Tomato Septoria Leaf Spot (Septoria lycopersici)",
        "description": "Destructive foliar fungus producing numerous small circular spots with grayish-white centers, dark brown borders, and tiny black fruiting pycnidia specks.",
        "symptoms": [
            "Numerous small circular spots (1/8 inch) with light gray centers and dark brown borders",
            "Tiny black specks (pycnidia) clearly visible in the center of mature spots under hand lens",
            "Leaves turn yellow around spots, curl, dry out, and drop prematurely from the bottom up",
            "Fruit is rarely infected directly, but severe defoliation leads to extensive sunscald"
        ],
        "treatment_recommendations": [
            "Apply Chlorothalonil 75% WP @ 2 g/L or Mancozeb 75% WP @ 2.5 g/L on 7-10 day intervals",
            "Spray Azoxystrobin + Difenoconazole or Pyraclostrobin during active blight pressure",
            "Prune off infected lower leaves as soon as initial symptoms appear",
            "Apply organic or plastic mulch beneath plants to prevent soil-splash spore dispersal"
        ],
        "preventive_measures": [
            "Practice a 3-year crop rotation away from solanaceous plants and horse nettle weeds",
            "Stake and cage tomato plants to keep foliage elevated off soil surface",
            "Plow under or remove and compost tomato vine debris post-harvest"
        ],
        "risk_level": "High"
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop_name": "Tomato",
        "disease_name": "Two-Spotted Spider Mite (Tetranychus urticae)",
        "description": "Microscopic arachnid pests that pierce plant cells on leaf undersides, producing fine yellow stippling, chlorosis, delicate silky webbing, and leaf bronzing.",
        "symptoms": [
            "Tiny yellow or white speckling/stippling on upper leaf surfaces",
            "Fine, delicate silky webbing visible on leaf undersides and shoot tips",
            "Leaves turn yellow, bronze, dry out, and drop under heavy infestation",
            "Stunted plant growth and reduced fruit yield during hot, dry weather conditions"
        ],
        "treatment_recommendations": [
            "Spray Abamectin 1.8% EC @ 0.5 mL/L or Spiromesifen 22.9% SC (Oberon) @ 1 mL/L",
            "Apply insecticidal soap or horticultural Neem Oil (Azadirachtin 10,000 ppm) @ 2 mL/L",
            "Release predatory biological biocontrol mites (Phytoseiulus persimilis or Neoseiulus californicus)",
            "Hose down dusty farm roads; dust favors rapid spider mite population outbreaks"
        ],
        "preventive_measures": [
            "Avoid excessive synthetic pyrethroid insecticides which eliminate beneficial mite predators",
            "Maintain optimal plant hydration; drought-stressed tomatoes attract heavy mite colonizations",
            "Isolate and discard heavily webbed infested nursery transplants before field planting"
        ],
        "risk_level": "Medium"
    },
    "Tomato___Target_Spot": {
        "crop_name": "Tomato",
        "disease_name": "Tomato Target Spot (Corynespora cassiicola)",
        "description": "Fungal pathogen causing brown circular lesions with concentric rings and yellow halos on leaves, stems, and sunken dark crater lesions on tomato fruit.",
        "symptoms": [
            "Small, circular brown lesions with faint concentric rings and light brown centers",
            "Lesions surrounded by a diffuse yellow halo; spots lack dark black rings of early blight",
            "Severe lesions coalesce, causing extensive blighting and foliage shedding",
            "Fruit exhibits sunken, dark brown, crater-like lesions that crack as fruit matures"
        ],
        "treatment_recommendations": [
            "Spray Azoxystrobin + Difenoconazole @ 1 mL/L or Boscalid @ 1 g/L",
            "Apply Chlorothalonil 75% WP @ 2 g/L or Copper Hydroxide on a 7-day preventive rotation",
            "Prune dense lower foliage to enhance air circulation and lower canopy humidity",
            "Stake plants and maintain mulch to prevent soil-splash contamination"
        ],
        "preventive_measures": [
            "Rotate crops with non-hosts (corn, sorghum, bahia grass) for at least 2 seasons",
            "Remove alternate weed hosts (such as wild poinsettia and commelina)",
            "Avoid overhead irrigation; utilize drip irrigation with balanced fertilizer delivery"
        ],
        "risk_level": "High"
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop_name": "Tomato",
        "disease_name": "Tomato Yellow Leaf Curl Virus (TYLCV, Begomovirus)",
        "description": "Devastating viral disease vectored by the Whitefly (Bemisia tabaci), resulting in severe upward leaf curling, yellowing, dwarfed bushy growth, and fruit drop.",
        "symptoms": [
            "Severe upward curling and cupping of leaflets with pronounced marginal yellowing (chlorosis)",
            "Marked reduction in leaf size ('little leaf' appearance)",
            "Stunted, bushy upright plant architecture with shortened internodes",
            "Heavy flower abscission (drop); plants infected early fail to produce marketable fruit"
        ],
        "treatment_recommendations": [
            "No chemical cure exists for viral infection; immediately rogue and destroy infected plants",
            "Control the Whitefly vector with systemic Acetamiprid 20% SP @ 0.5 g/L or Imidacloprid 17.8% SL @ 0.5 mL/L",
            "Spray Neem oil (Azadirachtin 1%) or insecticidal soaps on leaf undersides",
            "Install yellow sticky traps (15-20 traps/acre) to monitor and mass-trap adult whiteflies"
        ],
        "preventive_measures": [
            "Plant TYLCV-resistant or tolerant tomato hybrids (e.g., cultivars with Ty-1, Ty-2, or Ty-3 genes)",
            "Cover nursery seedlings with 50-mesh insect-proof netting before transplanting",
            "Maintain a host-free crop break of 4-6 weeks between solanaceous plantings"
        ],
        "risk_level": "Critical"
    },
    "Tomato___Tomato_mosaic_virus": {
        "crop_name": "Tomato",
        "disease_name": "Tomato Mosaic Virus (ToMV, Tobamovirus)",
        "description": "Highly stable, mechanically transmitted virus causing light-and-dark green mottled mosaic leaf patterns, blistering, 'fern-leaf' distortion, and internal fruit browning.",
        "symptoms": [
            "Light and dark green mottled mosaic patterns on leaves",
            "Leaf distortion including puckering, narrowing, or stringy 'fern-leaf' appearance",
            "Stunted plant growth and delayed blossom development",
            "Internal brown necrotic tissue inside tomato fruit walls (brown vascular ring)"
        ],
        "treatment_recommendations": [
            "No chemical viricides available; infected plants must be carefully removed and burned",
            "Wash hands and dip tools in 20% nonfat dry milk solution or 10% TSP between plants",
            "Prohibit tobacco use (smoking, chewing) anywhere near tomato greenhouses or fields",
            "Disinfect greenhouse benches, stakes, and pruning knives after each pruning pass"
        ],
        "preventive_measures": [
            "Plant certified ToMV-resistant cultivars with Tm-2 or Tm-2^2 resistance alleles",
            "Use only certified virus-free seed treated with trisodium phosphate (TSP) or dry heat (70°C for 3 days)",
            "Avoid handling plants unnecessarily during peak vegetative growth"
        ],
        "risk_level": "Critical"
    },
    "Tomato___healthy": {
        "crop_name": "Tomato",
        "disease_name": "Healthy Tomato Leaf (No Pathogen Detected)",
        "description": "The leaf shows optimal chlorophyll synthesis, normal serrated leaflet anatomy, intact pubescence, and zero evidence of bacterial spots, blight rings, or viral curling.",
        "symptoms": [
            "Deep green, well-developed compound leaflets with healthy glandular trichomes (hairs)",
            "Complete absence of necrotic spots, target rings, chlorotic halos, or curling",
            "Vigorous shoot growth with strong flower truss initiation"
        ],
        "treatment_recommendations": [
            "No chemical fungicides, bactericides, or treatments needed",
            "Maintain consistent drip irrigation to keep soil moisture uniform",
            "Supply balanced fertigation with calcium and potassium for blossom-end strength"
        ],
        "preventive_measures": [
            "Stake and prune lower sucker leaves to maintain air movement near ground",
            "Apply straw mulch to prevent soil splashing onto bottom foliage",
            "Conduct routine weekly scouting for early blight or whitefly presence"
        ],
        "risk_level": "None"
    }
}

class DiseaseModelService:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.model_type = "CNN Multi-Class Classifier (38 Classes / 14 Crops)"
        self.class_names: List[str] = []
        self.plants: List[str] = []
        self.plant_to_classes: Dict[str, List[str]] = {}
        self.class_to_disease: Dict[str, str] = {}
        self._load_class_mapping()
        self._check_and_load_model()

    def _resolve_path(self, relative_path: str) -> str:
        """Resolve a file path across possible root directories."""
        if os.path.isabs(relative_path) and os.path.exists(relative_path):
            return relative_path

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # backend/
        workspace_dir = os.path.dirname(base_dir) # AgriSaathi/

        candidates = [
            os.path.join(workspace_dir, relative_path),
            os.path.join(base_dir, relative_path),
            os.path.abspath(relative_path),
            # Direct fallbacks in Downloads if working locally
            os.path.join(r"C:\Users\ESWAR\Downloads", os.path.basename(relative_path)),
            os.path.join(r"C:\Users\ESWAR\Downloads\AgriSaathi", relative_path)
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return relative_path

    def _load_class_mapping(self):
        """Load class_mapping.json generated during training."""
        mapping_path = self._resolve_path(settings.CLASS_MAPPING_PATH)
        if os.path.exists(mapping_path):
            try:
                with open(mapping_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.class_names = data.get("class_names", [])
                self.plants = data.get("plants", [])
                self.plant_to_classes = data.get("plant_to_classes", {})
                self.class_to_disease = data.get("class_to_disease", {})
                logger.info(f"Loaded class mapping: {len(self.class_names)} classes across {len(self.plants)} plants.")
            except Exception as e:
                logger.error(f"Failed loading class mapping from {mapping_path}: {e}")
        else:
            logger.warning(f"Class mapping file not found at {mapping_path}")

    def _check_and_load_model(self):
        """Check for and load trained Keras CNN model."""
        model_path = self._resolve_path(settings.DISEASE_MODEL_PATH)
        if os.path.exists(model_path):
            try:
                import tensorflow as tf
                # Disable excessive TF logs
                os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
                logger.info(f"Loading trained plant disease model from {model_path}...")
                self.model = tf.keras.models.load_model(model_path)
                self.model_loaded = True
                logger.info(f"Successfully loaded model from {model_path}! Input shape: {self.model.input_shape}")
            except Exception as e:
                logger.error(f"Found model file at {model_path} but failed to load: {e}")
                self.model_loaded = False
        else:
            logger.warning(f"No model file found at '{model_path}'. Disease detection is operating in unconfigured mode.")
            self.model_loaded = False

    def validate_image(self, file_bytes: bytes, filename: str) -> Tuple[bool, str, Optional[Image.Image]]:
        """Validate uploaded image format, dimensions, and payload integrity."""
        max_size_bytes = 10 * 1024 * 1024  # 10 MB limit
        if len(file_bytes) > max_size_bytes:
            return False, "Image file size exceeds the 10 MB limit.", None
        
        allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        ext = os.path.splitext(filename.lower())[1]
        if ext not in allowed_extensions:
            return False, f"Unsupported file type '{ext}'. Allowed formats: JPG, JPEG, PNG, WEBP.", None
        
        try:
            image = Image.open(io.BytesIO(file_bytes))
            image.verify()
            image = Image.open(io.BytesIO(file_bytes))
            
            width, height = image.size
            if width < 32 or height < 32:
                return False, "Image resolution too low. Please upload an image of at least 32x32 pixels.", None
                
            return True, "Valid image", image
        except Exception as e:
            return False, f"Uploaded file is corrupt or not a valid image: {str(e)}", None

    def save_image(self, file_bytes: bytes, original_filename: str) -> Tuple[str, str]:
        """Save uploaded image to disk with a secure unique filename."""
        ext = os.path.splitext(original_filename.lower())[1] or ".jpg"
        unique_name = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(settings.UPLOAD_DIR, unique_name)
        
        with open(filepath, "wb") as f:
            f.write(file_bytes)
            
        relative_url = f"/uploads/disease_images/{unique_name}"
        return filepath, relative_url

    def _normalize_crop_name(self, raw_crop: Optional[str]) -> Optional[str]:
        """Normalize user input crop name to match plants in training dictionary."""
        if not raw_crop:
            return None
        c = raw_crop.strip().lower()
        if "all" in c or "auto" in c or "general" in c or "other" in c:
            return None
        
        mapping = {
            "apple": "Apple",
            "blueberry": "Blueberry",
            "cherry": "Cherry",
            "corn": "Corn (Maize)",
            "maize": "Corn (Maize)",
            "corn / maize": "Corn (Maize)",
            "corn (maize)": "Corn (Maize)",
            "grape": "Grape",
            "orange": "Orange",
            "peach": "Peach",
            "pepper": "Pepper (Bell)",
            "bell pepper": "Pepper (Bell)",
            "pepper (bell)": "Pepper (Bell)",
            "pepper, bell": "Pepper (Bell)",
            "potato": "Potato",
            "raspberry": "Raspberry",
            "soybean": "Soybean",
            "squash": "Squash",
            "strawberry": "Strawberry",
            "tomato": "Tomato"
        }
        for k, v in mapping.items():
            if k in c:
                return v
        return None

    async def predict(
        self,
        file_bytes: bytes,
        filename: str,
        crop_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze plant leaf image with multi-plant trained CNN model.
        Supports both crop-filtered species inference and global 38-class diagnosis.
        """
        # Step 1: Validate image
        is_valid, error_msg, pil_img = self.validate_image(file_bytes, filename)
        if not is_valid:
            return {
                "success": False,
                "message": error_msg,
                "model_configured": self.model_loaded
            }

        # Step 2: Save image for record & expert review
        file_path, image_url = self.save_image(file_bytes, filename)

        # Step 3: Check if trained model weights exist
        if not self.model_loaded or self.model is None:
            return {
                "success": True,
                "model_configured": False,
                "image_url": image_url,
                "image_path": file_path,
                "plant_name": crop_type or "Crop Leaf Sample",
                "predicted_disease": None,
                "confidence_score": None,
                "risk_level": "None",
                "message": (
                    "Image successfully uploaded and validated. "
                    "The AI CNN deep-learning model weights are currently unconfigured. "
                    "You may submit this image to an Agricultural Expert for clinical review."
                ),
                "visible_symptoms": [],
                "treatment_recommendations": [],
                "preventive_measures": [],
                "top_predictions": [],
                "top_probabilities": {}
            }

        # Step 4: Trained model inference
        try:
            import numpy as np
            
            # Input shape for full_plant_disease_model is (128, 128, 3)
            # Rescaling(1./255) is already the first layer in the Sequential model
            resized = pil_img.convert("RGB").resize((128, 128))
            img_arr = np.expand_dims(np.array(resized, dtype=np.float32), axis=0)

            raw_preds = self.model.predict(img_arr, verbose=0)[0]

            matched_plant = self._normalize_crop_name(crop_type)

            if matched_plant and matched_plant in self.plant_to_classes:
                # Mode A: User selected a specific crop variety
                candidate_classes = self.plant_to_classes[matched_plant]
                candidate_indices = [self.class_names.index(c) for c in candidate_classes if c in self.class_names]
                candidate_probs = [float(raw_preds[i]) for i in candidate_indices]

                total_p = sum(candidate_probs)
                if total_p > 0:
                    norm_probs = {c: float(p / total_p) for c, p in zip(candidate_classes, candidate_probs)}
                else:
                    norm_probs = {c: float(1.0 / len(candidate_classes)) for c in candidate_classes}

                top_class = max(norm_probs, key=norm_probs.get)
                conf_pct = round(norm_probs[top_class] * 100.0, 1)

                # Build top_predictions list sorted by probability
                top_predictions = []
                sorted_classes = sorted(norm_probs.keys(), key=lambda c: norm_probs[c], reverse=True)
                for c in sorted_classes:
                    d_name = self.class_to_disease.get(c, c)
                    p_val = round(norm_probs[c] * 100.0, 1)
                    top_predictions.append({
                        "condition": d_name,
                        "confidence_percentage": p_val,
                        "is_healthy": "healthy" in c.lower()
                    })

                top_probabilities = {self.class_to_disease.get(c, c): round(norm_probs[c] * 100.0, 1) for c in sorted_classes}

            else:
                # Mode B: Global / Auto-detect across all 38 classes
                top_idx = int(np.argmax(raw_preds))
                top_class = self.class_names[top_idx]
                conf_pct = round(float(raw_preds[top_idx]) * 100.0, 1)

                # Determine matched plant from class prefix
                matched_plant = top_class.split("___")[0].replace("_", " ").strip()

                # Get top 5 global predictions
                top_indices = np.argsort(raw_preds)[::-1][:5]
                top_predictions = []
                top_probabilities = {}
                for idx in top_indices:
                    c = self.class_names[idx]
                    p_val = round(float(raw_preds[idx]) * 100.0, 1)
                    d_name = self.class_to_disease.get(c, c)
                    plant_prefix = c.split("___")[0].replace("_", " ").strip()
                    label = f"{plant_prefix} - {d_name}" if "healthy" not in c.lower() else f"{plant_prefix} (Healthy)"
                    top_predictions.append({
                        "condition": label,
                        "confidence_percentage": p_val,
                        "is_healthy": "healthy" in c.lower()
                    })
                    top_probabilities[label] = p_val

            # Retrieve agronomic knowledge entry
            kb_entry = DISEASE_KNOWLEDGE_BASE.get(top_class)
            if not kb_entry:
                # Fallback to general healthy or disease item
                disease_label = self.class_to_disease.get(top_class, top_class.replace("_", " "))
                is_healthy = "healthy" in top_class.lower()
                kb_entry = {
                    "crop_name": matched_plant or "Plant Leaf Sample",
                    "disease_name": disease_label,
                    "description": f"Diagnosed {disease_label} for {matched_plant}." if not is_healthy else f"Healthy foliage detected for {matched_plant}.",
                    "symptoms": ["Visible symptomatic discoloration or stippling on leaf surface"] if not is_healthy else ["Uniform leaf coloration with intact margins"],
                    "treatment_recommendations": ["Consult local Krishi Vigyan Kendra (KVK) extension officer for site-specific treatment."] if not is_healthy else ["Maintain balanced irrigation and nutrient management."],
                    "preventive_measures": ["Practice crop rotation and field sanitation.", "Scout regularly for early warning signs."],
                    "risk_level": "Medium" if not is_healthy else "None"
                }

            return {
                "success": True,
                "model_configured": True,
                "image_url": image_url,
                "image_path": file_path,
                "plant_name": kb_entry["crop_name"],
                "predicted_disease": kb_entry["disease_name"],
                "confidence_score": conf_pct,
                "disease_description": kb_entry["description"],
                "visible_symptoms": kb_entry["symptoms"],
                "treatment_recommendations": kb_entry["treatment_recommendations"],
                "preventive_measures": kb_entry["preventive_measures"],
                "risk_level": kb_entry.get("risk_level", "Medium"),
                "top_predictions": top_predictions,
                "top_probabilities": top_probabilities,
                "message": f"Pathology diagnosed with {conf_pct}% confidence."
            }

        except Exception as e:
            logger.error(f"Inference error on CNN model: {e}", exc_info=True)
            return {
                "success": False,
                "model_configured": True,
                "message": f"Error running inference on model: {str(e)}"
            }

disease_service = DiseaseModelService()
