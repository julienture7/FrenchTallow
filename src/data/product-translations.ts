// Product translations for all supported languages
export interface ProductTranslations {
  name: string;
  scentBenefits: string;
}

export const productTranslations: Record<string, Record<string, ProductTranslations>> = {
  // English
  en: {
    lemon: { name: 'Lemon', scentBenefits: 'Uplifting, brightening' },
    coffee: { name: 'Coffee', scentBenefits: 'Energizing, rich aroma' },
    blood_orange: { name: 'Blood Orange', scentBenefits: 'Vibrant, revitalizing' },
    eucalyptus: { name: 'Eucalyptus', scentBenefits: 'Cooling, clearing' },
    pear: { name: 'Pear', scentBenefits: 'Gentle, subtly sweet' },
    pineapple: { name: 'Pineapple', scentBenefits: 'Tropical, brightening' },
    vanilla: { name: 'Vanilla', scentBenefits: 'Comforting, sweet' },
    lavender: { name: 'Lavender', scentBenefits: 'Calming, soothing' },
    bergamot: { name: 'Bergamot', scentBenefits: 'Uplifting, balancing' },
    rosemary: { name: 'Rosemary', scentBenefits: 'Stimulating, clarifying' },
    honey: { name: 'Honey', scentBenefits: 'Nourishing, golden' },
    lemongrass: { name: 'Lemongrass', scentBenefits: 'Purifying, fresh' },
    peach: { name: 'Peach', scentBenefits: 'Gentle, delicate' },
    unscented: { name: 'Unscented', scentBenefits: 'Pure, fragrance-free' },
    bulk: { name: '6-Pack Variety', scentBenefits: 'Best value, gift-ready' }
  },

  // French - Francais
  fr: {
    lemon: { name: 'Citron', scentBenefits: 'Revitalisant, eclaircissant' },
    coffee: { name: 'Cafe', scentBenefits: 'Energisant, arôme riche' },
    blood_orange: { name: 'Orange Rouge', scentBenefits: 'Vibrant, revigorant' },
    eucalyptus: { name: 'Eucalyptus', scentBenefits: 'Rafraichissant, purifiant' },
    pear: { name: 'Poire', scentBenefits: 'Doux, subtilement sucre' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropical, eclaircissant' },
    vanilla: { name: 'Vanille', scentBenefits: 'Reconfortant, doux' },
    lavender: { name: 'Lavande', scentBenefits: 'Calmant, apaisant' },
    bergamot: { name: 'Bergamote', scentBenefits: 'Revitalisant, equilibrant' },
    rosemary: { name: 'Romarin', scentBenefits: 'Stimulant, clarifiant' },
    honey: { name: 'Miel', scentBenefits: 'Nourrissant, dore' },
    lemongrass: { name: 'Citronnelle', scentBenefits: 'Purifiant, frais' },
    peach: { name: 'Peche', scentBenefits: 'Doux, delikat' },
    unscented: { name: 'Sans Parfum', scentBenefits: 'Pur, sans fragrance' },
    bulk: { name: 'Pack Variete 6', scentBenefits: 'Meilleur valeur, pret a offrir' }
  },

  // German - Deutsch
  de: {
    lemon: { name: 'Zitrone', scentBenefits: 'Aufhellend, erfrischend' },
    coffee: { name: 'Kaffee', scentBenefits: 'Energisierend, reiches Aroma' },
    blood_orange: { name: 'Blutorange', scentBenefits: 'Lebhaft, belebend' },
    eucalyptus: { name: 'Eukalyptus', scentBenefits: 'Kuhlend, befreiend' },
    pear: { name: 'Birne', scentBenefits: 'Sanft, subtil suss' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropisch, aufhellend' },
    vanilla: { name: 'Vanille', scentBenefits: 'Wohlend, suss' },
    lavender: { name: 'Lavendel', scentBenefits: 'Beruhigend, lindernd' },
    bergamot: { name: 'Bergamotte', scentBenefits: 'Aufhellend, ausgleichend' },
    rosemary: { name: 'Rosmarin', scentBenefits: 'Anregend, klarend' },
    honey: { name: 'Honig', scentBenefits: 'Nahrhaft, golden' },
    lemongrass: { name: 'Zitronengras', scentBenefits: 'Reinigend, frisch' },
    peach: { name: 'Pfirsich', scentBenefits: 'Sanft, zart' },
    unscented: { name: 'Unparfumiert', scentBenefits: 'Rein, ohne Duftstoffe' },
    bulk: { name: '6er-Variationspack', scentBenefits: 'Bester Wert, geschenkfertig' }
  },

  // Spanish - Espanol
  es: {
    lemon: { name: 'Limon', scentBenefits: 'Energizante, luminoso' },
    coffee: { name: 'Cafe', scentBenefits: 'Energizante, aroma rico' },
    blood_orange: { name: 'Naranja Sanguina', scentBenefits: 'Vibrante, revigorizante' },
    eucalyptus: { name: 'Eucalipto', scentBenefits: 'Refrescante, despejante' },
    pear: { name: 'Pera', scentBenefits: 'Suave, sutilmente dulce' },
    pineapple: { name: 'Pina', scentBenefits: 'Tropical, luminoso' },
    vanilla: { name: 'Vainilla', scentBenefits: 'Reconfortante, dulce' },
    lavender: { name: 'Lavanda', scentBenefits: 'Calmante, relajante' },
    bergamot: { name: 'Bergamota', scentBenefits: 'Energizante, equilibrante' },
    rosemary: { name: 'Romero', scentBenefits: 'Estimulante, clarificante' },
    honey: { name: 'Miel', scentBenefits: 'Nutritivo, dorado' },
    lemongrass: { name: 'Hierba de Limon', scentBenefits: 'Purificante, fresco' },
    peach: { name: 'Melocoton', scentBenefits: 'Suave, delicado' },
    unscented: { name: 'Sin Perfume', scentBenefits: 'Puro, sin fragancia' },
    bulk: { name: 'Pack Variedad 6', scentBenefits: 'Mejor valor, listo para regalar' }
  },

  // Italian - Italiano
  it: {
    lemon: { name: 'Limone', scentBenefits: 'Rallegrante, illuminante' },
    coffee: { name: 'Caffe', scentBenefits: 'Energizzante, aroma ricco' },
    blood_orange: { name: 'Arancia Sanguinella', scentBenefits: 'Vibrante, rivitalizzante' },
    eucalyptus: { name: 'Eucalipto', scentBenefits: 'Rinfrescante, purificante' },
    pear: { name: 'Pera', scentBenefits: 'Delicato, lievemente dolce' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropicale, illuminante' },
    vanilla: { name: 'Vaniglia', scentBenefits: 'Rassicurante, dolce' },
    lavender: { name: 'Lavanda', scentBenefits: 'Calmante, lenitivo' },
    bergamot: { name: 'Bergamotto', scentBenefits: 'Rallegrante, equilibrante' },
    rosemary: { name: 'Rosmarino', scentBenefits: 'Stimolante, chiarificante' },
    honey: { name: 'Miele', scentBenefits: 'Nutriente, dorato' },
    lemongrass: { name: 'Citronella', scentBenefits: 'Purificante, fresco' },
    peach: { name: 'Pesca', scentBenefits: 'Delicato, fine' },
    unscented: { name: 'Non Profumato', scentBenefits: 'Puro, senza fragranza' },
    bulk: { name: 'Pack Varieta 6', scentBenefits: 'Miglior valore, pronto per regalo' }
  },

  // Portuguese - Portugues
  pt: {
    lemon: { name: 'Limao', scentBenefits: 'Revitalizante, iluminador' },
    coffee: { name: 'Cafe', scentBenefits: 'Energizante, aroma rico' },
    blood_orange: { name: 'Laranja Sangunea', scentBenefits: 'Vibrante, revigorante' },
    eucalyptus: { name: 'Eucalipto', scentBenefits: 'Refrescante, purificador' },
    pear: { name: 'Pera', scentBenefits: 'Suave, sutilmente doce' },
    pineapple: { name: 'Abacaxi', scentBenefits: 'Tropical, iluminador' },
    vanilla: { name: 'Baunilha', scentBenefits: 'Confortante, doce' },
    lavender: { name: 'Lavanda', scentBenefits: 'Calmante, suavizante' },
    bergamot: { name: 'Bergamota', scentBenefits: 'Revitalizante, equilibrante' },
    rosemary: { name: 'Alecrim', scentBenefits: 'Estimulante, clarificante' },
    honey: { name: 'Mel', scentBenefits: 'Nutritivo, dourado' },
    lemongrass: { name: 'Capim-limao', scentBenefits: 'Purificante, fresco' },
    peach: { name: 'Pessego', scentBenefits: 'Suave, delicado' },
    unscented: { name: 'Sem Perfume', scentBenefits: 'Puro, sem fragrancia' },
    bulk: { name: 'Pack Variedade 6', scentBenefits: 'Melhor valor, pronto para presente' }
  },

  // Dutch - Nederlands
  nl: {
    lemon: { name: 'Citroen', scentBenefits: 'Verhelderend, opfrissend' },
    coffee: { name: 'Koffie', scentBenefits: 'Energiserend, rijk aroma' },
    blood_orange: { name: 'Bloedsinaasappel', scentBenefits: 'Levendig, verkwikkend' },
    eucalyptus: { name: 'Eucalyptus', scentBenefits: 'Verkoelend, zuiverend' },
    pear: { name: 'Peer', scentBenefits: 'Zacht, subtiel zoet' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropisch, verhelderend' },
    vanilla: { name: 'Vanille', scentBenefits: 'Troostend, zoet' },
    lavender: { name: 'Lavendel', scentBenefits: 'Kalmerend, verzachtend' },
    bergamot: { name: 'Bergamot', scentBenefits: 'Verhelderend, balancerend' },
    rosemary: { name: 'Rozemarijn', scentBenefits: 'Stimulerend, verhelderend' },
    honey: { name: 'Honing', scentBenefits: 'Voedend, goudkleurig' },
    lemongrass: { name: 'Citroengras', scentBenefits: 'Zuiverend, fris' },
    peach: { name: 'Perzik', scentBenefits: 'Zacht, delicaat' },
    unscented: { name: 'Ongeparfumeerd', scentBenefits: 'Puur, geur-vrij' },
    bulk: { name: '6-Voudig Variatiepakket', scentBenefits: 'Beste waarde, cadeau-klaar' }
  },

  // Polish - Polski
  pl: {
    lemon: { name: 'Cytryna', scentBenefits: 'Podnoszacy, rozjasniajacy' },
    coffee: { name: 'Kawa', scentBenefits: 'Energizujacy, bogaty aromat' },
    blood_orange: { name: 'Pomarancza Krwawa', scentBenefits: 'Zywy, odmladzajacy' },
    eucalyptus: { name: 'Eukaliptus', scentBenefits: 'Chlodzacy, oczyszczajacy' },
    pear: { name: 'Gruszka', scentBenefits: 'Lagodny, subtelnie slodki' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropikalny, rozjasniajacy' },
    vanilla: { name: 'Wanilia', scentBenefits: 'Kojacy, slodki' },
    lavender: { name: 'Lawenda', scentBenefits: 'Kojacy, uspokajajacy' },
    bergamot: { name: 'Bergamotka', scentBenefits: 'Podnoszacy, rownowazacy' },
    rosemary: { name: 'Rozmaryn', scentBenefits: 'Pobudzajacy, wyjasniajacy' },
    honey: { name: 'Miod', scentBenefits: 'Odzywczy, zloty' },
    lemongrass: { name: 'Trawa Cytrynowa', scentBenefits: 'Oczyszczajacy, swiezy' },
    peach: { name: 'Brzoskwinia', scentBenefits: 'Lagodny, delikatny' },
    unscented: { name: 'Bez Zapachu', scentBenefits: 'Czysty, bez zapachu' },
    bulk: { name: 'Zestaw 6 w Rodzajach', scentBenefits: 'Najlepsza wartosc, gotowy na prezent' }
  },

  // Swedish - Svenska
  sv: {
    lemon: { name: 'Citron', scentBenefits: 'Upliftande, uppfriskande' },
    coffee: { name: 'Kaffe', scentBenefits: 'Energiserande, rik arom' },
    blood_orange: { name: 'Blodapelsin', scentBenefits: 'Livlig, vitaliserande' },
    eucalyptus: { name: 'Eukalyptus', scentBenefits: 'Svalkande, rensande' },
    pear: { name: 'Paron', scentBenefits: 'Mild, diskret sott' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropisk, uppfriskande' },
    vanilla: { name: 'Vanilj', scentBenefits: 'Trostande, sott' },
    lavender: { name: 'Lavendel', scentBenefits: 'Lugnande, lugnande' },
    bergamot: { name: 'Bergamott', scentBenefits: 'Upliftande, balanserande' },
    rosemary: { name: 'Rosmarin', scentBenefits: 'Stimulerande, klargorande' },
    honey: { name: 'Honung', scentBenefits: 'Narande, gyllene' },
    lemongrass: { name: 'Citrongras', scentBenefits: 'Rensande, frisk' },
    peach: { name: 'Persika', scentBenefits: 'Mild, len' },
    unscented: { name: 'Doftfri', scentBenefits: 'Ren, luktfril' },
    bulk: { name: '6-Pack Variation', scentBenefits: 'Bast varde, presentklar' }
  },

  // Danish - Dansk
  da: {
    lemon: { name: 'Citron', scentBenefits: 'Opliftende, lysnende' },
    coffee: { name: 'Kaffe', scentBenefits: 'Energiserende, rig aroma' },
    blood_orange: { name: 'Blodappelsin', scentBenefits: 'Vibrerende, vitaliserende' },
    eucalyptus: { name: 'Eukalyptus', scentBenefits: 'Kolende, klarlende' },
    pear: { name: 'Pare', scentBenefits: 'Blid, subtilt sod' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropisk, lysnende' },
    vanilla: { name: 'Vanilje', scentBenefits: 'Trostende, sod' },
    lavender: { name: 'Lavendel', scentBenefits: 'Beroligende, lindrende' },
    bergamot: { name: 'Bergamot', scentBenefits: 'Opliftende, balancerende' },
    rosemary: { name: 'Rosmarin', scentBenefits: 'Stimulerende, klargorende' },
    honey: { name: 'Honning', scentBenefits: 'Narende, gylden' },
    lemongrass: { name: 'Citrongras', scentBenefits: 'Rensende, frisk' },
    peach: { name: 'Fersken', scentBenefits: 'Blid, delikat' },
    unscented: { name: 'Uparfumeret', scentBenefits: 'Ren, duftfri' },
    bulk: { name: '6-Stk. Sorteret', scentBenefits: 'Bedste varde, gaveklar' }
  },

  // Finnish - Suomi
  fi: {
    lemon: { name: 'Sitruuna', scentBenefits: 'Kohottava, kirkastava' },
    coffee: { name: 'Kahvi', scentBenefits: 'Energisoiva, rikas tuoksu' },
    blood_orange: { name: 'Verappelsiini', scentBenefits: 'Eloisa, virkistava' },
    eucalyptus: { name: 'Eukalyptus', scentBenefits: 'Viilentava, puhdistava' },
    pear: { name: 'Paryna', scentBenefits: 'Lempea, hienostuneen makea' },
    pineapple: { name: 'Ananas', scentBenefits: 'Trooppinen, kirkastava' },
    vanilla: { name: 'Vanilja', scentBenefits: 'Lohttuva, makea' },
    lavender: { name: 'Laventeli', scentBenefits: 'Rauhoittava, rauhoittava' },
    bergamot: { name: 'Bergamotti', scentBenefits: 'Kohottava, tasapainottava' },
    rosemary: { name: 'Rosmariini', scentBenefits: 'Stimuloiva, selkeyttava' },
    honey: { name: 'Hunaja', scentBenefits: 'Ravitseva, kultainen' },
    lemongrass: { name: 'Sitruunaruoho', scentBenefits: 'Puhdistava, tuore' },
    peach: { name: 'Persikka', scentBenefits: 'Lempea, hienostunut' },
    unscented: { name: 'Hajusteeton', scentBenefits: 'Puhdas, hajuton' },
    bulk: { name: '6-Pack Monipuolinen', scentBenefits: 'Paras arvo, lahjavalmis' }
  },

  // Greek - Ellinika
  el: {
    lemon: { name: 'Лем▌нй', scentBenefits: 'Анελκυσтик▌, φωτειн▌' },
    coffee: { name: 'Καφн▌', scentBenefits: 'Ενεργιακ▌, πλο▌σιο ▌ρωμα' },
    blood_orange: { name: 'Αιματωμн▌νο Πορτοκ▄λι', scentBenefits: 'Ζωνταν▄, αναζωογονητικ▄' },
    eucalyptus: { name: 'Ε▌καλυπτος', scentBenefits: 'Δροσιστικ▄, καθαριστικ▄' },
    pear: { name: 'Αχλ▄δι', scentBenefits: 'Απαλ▄, διακριτικ▄ γλυκ▄' },
    pineapple: { name: 'Αναν▄ς', scentBenefits: 'Τροπικ▄, φωτειν▄' },
    vanilla: { name: 'Βανн▌λια', scentBenefits: 'Ανακουφιστικ▄, γλυκ▄' },
    lavender: { name: 'Λεβ▄ντα', scentBenefits: 'Γαληνευτικ▄, καταπραυντικ▄' },
    bergamot: { name: 'Μπεργαμ▄τη', scentBenefits: 'Ανελκυστικ▄, εξισορροπητικ▄' },
    rosemary: { name: 'Ρομαρн▄να', scentBenefits: 'Διεγεριντικ▄, διευκρινιστικ▄' },
    honey: { name: 'Μн▄λι', scentBenefits: 'Θρεπτικ▄, χρυσ▄' },
    lemongrass: { name: 'Λεμον▄χορτο', scentBenefits: 'Καθαριστικ▄, φρн▌σκο' },
    peach: { name: 'Ροδ▄κινο', scentBenefits: 'Απαλ▄, λεπτ▄' },
    unscented: { name: 'Χωρн▌ς ▌ρωμα', scentBenefits: 'Αυθ▄ντομο, χωρн▌ς ▌ρωμα' },
    bulk: { name: 'Πακн▄το Ποικιλн▌ας 6', scentBenefits: 'Καλ▄τερη τιμн▄, н▄τοιμο για δ▶ρο' }
  },

  // Czech - Cestina
  cs: {
    lemon: { name: 'Citron', scentBenefits: 'Povzbuzujici, rozjasnujici' },
    coffee: { name: 'Kava', scentBenefits: 'Energizujici, bohat vona' },
    blood_orange: { name: 'Krav Pomeranc', scentBenefits: 'Ziv, omlazujici' },
    eucalyptus: { name: 'Eukalyptus', scentBenefits: 'Chlazici, cistici' },
    pear: { name: 'Hruska', scentBenefits: 'Jemny, jemne sladky' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropicky, rozjasnujici' },
    vanilla: { name: 'Vanilka', scentBenefits: 'Uklidnujici, sladky' },
    lavender: { name: 'Levandule', scentBenefits: 'Uklidnujici, zklidnujici' },
    bergamot: { name: 'Bergamot', scentBenefits: 'Povzbuzujici, vyrovnavaci' },
    rosemary: { name: 'Rozmaryna', scentBenefits: 'Podnetny, objasnujici' },
    honey: { name: 'Med', scentBenefits: 'Vyzivny, zlaty' },
    lemongrass: { name: 'Citronova trava', scentBenefits: 'Cistici, svezi' },
    peach: { name: 'Broskev', scentBenefits: 'Jemny, delicatny' },
    unscented: { name: 'Bez Vune', scentBenefits: 'Cisty, bez vune' },
    bulk: { name: 'Baleni 6 Variety', scentBenefits: 'Nejlepsi hodnota, hotovy darek' }
  },

  // Romanian - Romana
  ro: {
    lemon: { name: 'Lamaie', scentBenefits: 'Ridicator, inseninator' },
    coffee: { name: 'Cafea', scentBenefits: 'Energizant, arom bogat' },
    blood_orange: { name: 'Portocala Sanguie', scentBenefits: 'Vibrant, revigorant' },
    eucalyptus: { name: 'Eucalipt', scentBenefits: 'Racoritor, clarificator' },
    pear: { name: 'Para', scentBenefits: 'Blind, subtii dulce' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropical, inseninator' },
    vanilla: { name: 'Vanilie', scentBenefits: 'Linistitor, dulce' },
    lavender: { name: 'Lavanda', scentBenefits: 'Calmant, linistitor' },
    bergamot: { name: 'Bergamota', scentBenefits: 'Ridicator, echilibrant' },
    rosemary: { name: 'Rozmarin', scentBenefits: 'Stimulant, clarificator' },
    honey: { name: 'Miere', scentBenefits: 'Hranitor, auriu' },
    lemongrass: { name: 'Lemongrass', scentBenefits: 'Curatire, proaspat' },
    peach: { name: 'Piersica', scentBenefits: 'Blind, delicat' },
    unscented: { name: 'Fara Parfum', scentBenefits: 'Pur, fara parfum' },
    bulk: { name: 'Pachet Varietate 6', scentBenefits: 'Cea mai buna valoare, pregatit pentru cadou' }
  },

  // Hungarian - Magyar
  hu: {
    lemon: { name: 'Citrom', scentBenefits: 'Feldobo, fenypotlo' },
    coffee: { name: 'Kave', scentBenefits: 'Energizalo, gazdag aroma' },
    blood_orange: { name: 'Vernarancs', scentBenefits: 'Eletkedv, ujjaeleiszto' },
    eucalyptus: { name: 'Eukaliptusz', scentBenefits: 'Husito, tisztito' },
    pear: { name: 'Korte', scentBenefits: 'Gyenged, finoman edes' },
    pineapple: { name: 'Ananasz', scentBenefits: 'Tropusi, fenypotlo' },
    vanilla: { name: 'Vanilia', scentBenefits: 'Vigasztalo, edes' },
    lavender: { name: 'Levendula', scentBenefits: 'Nyugtato, megnugtato' },
    bergamot: { name: 'Bergamott', scentBenefits: 'Feldobo, kiegyensulyozo' },
    rosemary: { name: 'Rozmaring', scentBenefits: 'Osztonzo, tisztazo' },
    honey: { name: 'Mez', scentBenefits: 'Taplo, arany' },
    lemongrass: { name: 'Citromfu', scentBenefits: 'Tisztito, friss' },
    peach: { name: 'Barack', scentBenefits: 'Gyenged, finom' },
    unscented: { name: 'Szagtalan', scentBenefits: 'Tiszta, szagmentes' },
    bulk: { name: '6-Variacios Csomag', scentBenefits: 'Legjobb ertek, ajandek-kesz' }
  },

  // Slovak - Slovencina
  sk: {
    lemon: { name: 'Citron', scentBenefits: 'Povzbudzuci, zjasujuci' },
    coffee: { name: 'Kava', scentBenefits: 'Energizuci, bohat vuna' },
    blood_orange: { name: 'Krvava Pomaranc', scentBenefits: 'Zivy, omladzujuci' },
    eucalyptus: { name: 'Eukalyptus', scentBenefits: 'Chladiaci, cistiace' },
    pear: { name: 'Hruska', scentBenefits: 'Jemny, jemne sladky' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropicky, zjasujuci' },
    vanilla: { name: 'Vanilka', scentBenefits: 'Ukludujuci, sladky' },
    lavender: { name: 'Levandula', scentBenefits: 'Ukludujuci, zkludujuci' },
    bergamot: { name: 'Bergamot', scentBenefits: 'Povzbudzuci, vyrovnavaci' },
    rosemary: { name: 'Rozmarin', scentBenefits: 'Podnetny, objasnujuci' },
    honey: { name: 'Med', scentBenefits: 'Vyzivny, zlaty' },
    lemongrass: { name: 'Citronova trava', scentBenefits: 'Cistiace, sviezi' },
    peach: { name: 'Broskya', scentBenefits: 'Jemny, delikatny' },
    unscented: { name: 'Bez Vune', scentBenefits: 'Cisty, bez vune' },
    bulk: { name: '6-Balik Variacie', scentBenefits: 'Najlepsia hodnota, hotovy darek' }
  },

  // Bulgarian - Balgarski
  bg: {
    lemon: { name: 'Лимон', scentBenefits: 'Повдигащ, изсветляващ' },
    coffee: { name: 'Кафе', scentBenefits: 'Енергизиращ, богат аромат' },
    blood_orange: { name: 'Кръвава Портокал', scentBenefits: 'Жив, обновяващ' },
    eucalyptus: { name: 'Евкалипт', scentBenefits: 'Охлаждащ, почистващ' },
    pear: { name: 'Круша', scentBenefits: 'Нежен, нежно сладък' },
    pineapple: { name: 'Ананас', scentBenefits: 'Тропически, изсветляващ' },
    vanilla: { name: 'Ванилия', scentBenefits: 'Успокояващ, сладък' },
    lavender: { name: 'Лавандула', scentBenefits: 'Успокояващ, успокояващ' },
    bergamot: { name: 'Бергамот', scentBenefits: 'Повдигащ, балансиращ' },
    rosemary: { name: 'Розмарин', scentBenefits: 'Стимулиращ, изясняващ' },
    honey: { name: 'Мед', scentBenefits: 'Хранителен, златен' },
    lemongrass: { name: 'Лимонова трева', scentBenefits: 'Почистващ, свеж' },
    peach: { name: 'Праскова', scentBenefits: 'Нежен, деликатен' },
    unscented: { name: 'Без Аромат', scentBenefits: 'Чист, без аромат' },
    bulk: { name: '6-Пакет Вариетет', scentBenefits: 'Най-добра стойност, готов за подарък' }
  },

  // Croatian - Hrvatski
  hr: {
    lemon: { name: 'Limun', scentBenefits: 'Podizanje, osvjetljivanje' },
    coffee: { name: 'Kava', scentBenefits: 'Energiziranje, bogati okus' },
    blood_orange: { name: 'Krvava Naranca', scentBenefits: 'Zivahan, osvjezujuca' },
    eucalyptus: { name: 'Eukaliptus', scentBenefits: 'Hladno, ciscenje' },
    pear: { name: 'Kruska', scentBenefits: 'Blag, suptilno sladak' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropsko, osvjetljivanje' },
    vanilla: { name: 'Vanilija', scentBenefits: 'Uteha, slatko' },
    lavender: { name: 'Lavanda', scentBenefits: 'Smirenje, umirenje' },
    bergamot: { name: 'Bergamot', scentBenefits: 'Podizanje, balansiranje' },
    rosemary: { name: 'Ruzmarin', scentBenefits: 'Poticanje, razjasnjivanje' },
    honey: { name: 'Med', scentBenefits: 'Hranjivo, zlatno' },
    lemongrass: { name: 'Limeta trava', scentBenefits: 'Ciscenje, svjeze' },
    peach: { name: 'Breskva', scentBenefits: 'Blag, njezan' },
    unscented: { name: 'Bez Mirisa', scentBenefits: 'Cisto, bez mirisa' },
    bulk: { name: '6-Pack Raznolikost', scentBenefits: 'Najbolja vrijednost, spremno za poklon' }
  },

  // Slovenian - Slovencina
  sl: {
    lemon: { name: 'Limona', scentBenefits: 'Dvigujoca, osvetljujoca' },
    coffee: { name: 'Kava', scentBenefits: 'Energiziranje, bogat vonj' },
    blood_orange: { name: 'Krvna Pomarancna', scentBenefits: 'Zivahno, osvezuje' },
    eucalyptus: { name: 'Evkalipt', scentBenefits: 'Hlajenje, ciscenje' },
    pear: { name: 'Hruska', scentBenefits: 'Mehko, subtilno sladko' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropsko, osvetljujoca' },
    vanilla: { name: 'Vanilija', scentBenefits: 'Pocustitev, sladko' },
    lavender: { name: 'Lavanda', scentBenefits: 'Umirjujoca, pomirjoca' },
    bergamot: { name: 'Bergamot', scentBenefits: 'Dvigujoca, uravnotezujoce' },
    rosemary: { name: 'Rozmarin', scentBenefits: 'Stimuliranje, razjasnjevanje' },
    honey: { name: 'Med', scentBenefits: 'Hranljivo, zlato' },
    lemongrass: { name: 'Limonska trava', scentBenefits: 'Ciscenje, sveze' },
    peach: { name: 'Breskev', scentBenefits: 'Mehko, obcutljivo' },
    unscented: { name: 'Brez Vonja', scentBenefits: 'Cisto, brez vonja' },
    bulk: { name: '6-Pack Razlicnost', scentBenefits: 'Najboljsa vrednost, pripravljeno za darilo' }
  },

  // Lithuanian - Lietuviu
  lt: {
    lemon: { name: 'Citrina', scentBenefits: 'Keliancio, sviesinamo' },
    coffee: { name: 'Kava', scentBenefits: 'Energizuojantis, turtingas aromatas' },
    blood_orange: { name: 'Kraujinga Apelsina', scentBenefits: 'Gyvybingas, atgaivinantis' },
    eucalyptus: { name: 'Eukaliptas', scentBenefits: 'Vesinantis, valantis' },
    pear: { name: 'Kriause', scentBenefits: 'Ramus, subtiliai saldukas' },
    pineapple: { name: 'Ananasas', scentBenefits: 'Tropinis, sviesinantis' },
    vanilla: { name: 'Vanile', scentBenefits: 'Guodzioji, saldi' },
    lavender: { name: 'Levanda', scentBenefits: 'Raminantis, ramunantis' },
    bergamot: { name: 'Bergamote', scentBenefits: 'Keliancio, balansuojantis' },
    rosemary: { name: 'Rozmarinas', scentBenefits: 'Stimuliuojantis, aiskinantis' },
    honey: { name: 'Medus', scentBenefits: 'Maitinantis, auksinis' },
    lemongrass: { name: 'Citronine zole', scentBenefits: 'Valantis, svezas' },
    peach: { name: 'Persikas', scentBenefits: 'Ramus, delikatesiskas' },
    unscented: { name: 'Bez Kvapo', scentBenefits: 'Tikras, be kvapo' },
    bulk: { name: '6-Pack Ivyrove', scentBenefits: 'Geriausia verte, dovanu paruostas' }
  },

  // Latvian - Latviesu
  lv: {
    lemon: { name: 'Citrons', scentBenefits: 'Upliftinos, gaisinos' },
    coffee: { name: 'Kafija', scentBenefits: 'Energizos, bagats aromats' },
    blood_orange: { name: 'Asins Apelsins', scentBenefits: 'Dzivigs, atjaunojos' },
    eucalyptus: { name: 'Eikalipts', scentBenefits: 'Atdzesojos, tiris' },
    pear: { name: 'Abols', scentBenefits: 'Maigs, subtiliti sals' },
    pineapple: { name: 'Ananass', scentBenefits: 'Tropisks, gaisinos' },
    vanilla: { name: 'Vanila', scentBenefits: 'Majos, sals' },
    lavender: { name: 'Lavanda', scentBenefits: 'Rimjojos, majos' },
    bergamot: { name: 'Bergamotes', scentBenefits: 'Upliftinos, lidzsvaroos' },
    rosemary: { name: 'Rozmarins', scentBenefits: 'Stimulejos, skaidros' },
    honey: { name: 'Mes', scentBenefits: 'Baroos, zeltains' },
    lemongrass: { name: 'Citronu zale', scentBenefits: 'Atiros, svaigs' },
    peach: { name: 'Persiks', scentBenefits: 'Maigs, smalks' },
    unscented: { name: 'Bez Smarzas', scentBenefits: 'Tirs, bez smarzas' },
    bulk: { name: '6-Komplekts Varietetes', scentBenefits: 'Laka vertiba, davanu gatavs' }
  },

  // Estonian - Eesti
  et: {
    lemon: { name: 'Sidrun', scentBenefits: 'Ulevuse toov, heledus' },
    coffee: { name: 'Kohv', scentBenefits: 'Energiseeriv, rikas lohn' },
    blood_orange: { name: 'Veri Apelsin', scentBenefits: 'Vibrantne, elavdav' },
    eucalyptus: { name: 'Eukalupt', scentBenefits: 'Jahutav, puhastav' },
    pear: { name: 'Pirn', scentBenefits: 'Leebe, peenelt magus' },
    pineapple: { name: 'Ananass', scentBenefits: 'Troopiline, heledus' },
    vanilla: { name: 'Vanill', scentBenefits: 'Rahustav, magus' },
    lavender: { name: 'Lavendel', scentBenefits: 'Rahustav, leevendav' },
    bergamot: { name: 'Bergamott', scentBenefits: 'Ulevuse toov, tasakaalustav' },
    rosemary: { name: 'Rosmariin', scentBenefits: 'Stimuleeriv, selgitav' },
    honey: { name: 'Mets', scentBenefits: 'Toitev, kuldne' },
    lemongrass: { name: 'Sidrunihein', scentBenefits: 'Puhastav, varske' },
    peach: { name: 'Virsik', scentBenefits: 'Leebe, peen' },
    unscented: { name: 'Lohnata', scentBenefits: 'Puhas, lohnatu' },
    bulk: { name: '6-Komplekt Mitmekesisus', scentBenefits: 'Parim vaartus, kingiks valmis' }
  },

  // Maltese - Malti
  mt: {
    lemon: { name: 'Lumin', scentBenefits: 'Uplifting, hadif' },
    coffee: { name: 'Kafe', scentBenefits: 'Enerzzanti, aroma rikk' },
    blood_orange: { name: 'Larin tad-Demm', scentBenefits: 'Vibranti, rinvigoranti' },
    eucalyptus: { name: 'Ewkalittus', scentBenefits: 'Frisk, afil' },
    pear: { name: 'Laring', scentBenefits: 'Gentili, hlew suttili' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropikali, hadif' },
    vanilla: { name: 'Vanilla', scentBenefits: 'Kulwimm, hlew' },
    lavender: { name: 'Lavanda', scentBenefits: 'Kalmanti, soothing' },
    bergamot: { name: 'Bergamot', scentBenefits: 'Uplifting, bilangati' },
    rosemary: { name: 'Rosermary', scentBenefits: 'Stimolanti, arifikanti' },
    honey: { name: 'Hasel', scentBenefits: 'Nutrijenti, deheb' },
    lemongrass: { name: 'Lemongrass', scentBenefits: 'Purifikanti, frisk' },
    peach: { name: 'Hawh', scentBenefits: 'Gentili, delikat' },
    unscented: { name: 'Bla Xjuh', scentBenefits: 'Pur, bla fragranza' },
    bulk: { name: '6-Pack Varjeta', scentBenefits: 'Ahjar valur, rady ghal rigal' }
  },

  // Irish - Gaeilge
  ga: {
    lemon: { name: 'Liom', scentBenefits: 'Uplifting, soilsigh' },
    coffee: { name: 'Cafe', scentBenefits: 'Energizing, bholadh saibhir' },
    blood_orange: { name: 'Oriste Fola', scentBenefits: 'Beo, athbheochan' },
    eucalyptus: { name: 'Eiclioptas', scentBenefits: 'Fionuar, glan' },
    pear: { name: 'Piorra', scentBenefits: 'Gentle, milis gothan' },
    pineapple: { name: 'Ananas', scentBenefits: 'Tropaicigh, soilsigh' },
    vanilla: { name: 'Vanilla', scentBenefits: 'Suaithneach, milis' },
    lavender: { name: 'Labhandar', scentBenefits: 'Suaithneach, sugach' },
    bergamot: { name: 'Beargamos', scentBenefits: 'Uplifting, cothrom' },
    rosemary: { name: 'Rois', scentBenefits: 'Stiuguil, soilsi' },
    honey: { name: 'Miel', scentBenefits: 'Cotha, ir' },
    lemongrass: { name: 'Fear Lemon', scentBenefits: 'Glan, ur' },
    peach: { name: 'Peacha', scentBenefits: 'Gentle, deich' },
    unscented: { name: 'Gan Boladh', scentBenefits: 'Glan, gan bholadh' },
    bulk: { name: '6-Pack Eagsail', scentBenefits: 'Luach is fearr, reidh bronntanais' }
  }
};

// Get product translation for a specific product and language
export function getProductTranslation(productId: string, lang: string): ProductTranslations {
  const langTranslations = productTranslations[lang] || productTranslations.en;
  const product = langTranslations[productId as keyof typeof langTranslations];
  return product || { name: productId, scentBenefits: '' };
}

// Get all product translations for a language
export function getProductTranslations(lang: string): Record<string, ProductTranslations> {
  return productTranslations[lang] || productTranslations.en;
}
