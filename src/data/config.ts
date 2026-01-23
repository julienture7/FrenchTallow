// Site configuration
export const site = {
  name: 'FrenchTallowSoap',
  tagline: 'Ancestral Beauty, Modern Results',
  baseUrl: 'https://frenchtallow.com',
  etsyShop: 'https://www.etsy.com/shop/FrenchTallowSoap'
};

// Product data
export interface Product {
  name: string;
  etsyTitle: string;
  image: string;
  link: string;
  scentBenefits: string;
  price: number;
  category: 'citrus' | 'warm' | 'herbal' | 'floral';
}

export const products: Record<string, Product> = {
  lemon: {
    name: 'Lemon',
    etsyTitle: 'Whipped Tallow Balm Lemon, Zesty Body Butter',
    image: 'whipped-tallow-cream-lemon.png',
    link: 'https://www.etsy.com/listing/4436050638/whipped-tallow-balm-lemon-zesty-body',
    scentBenefits: 'Uplifting, brightening',
    price: 21,
    category: 'citrus'
  },
  coffee: {
    name: 'Coffee',
    etsyTitle: 'Whipped Tallow Balm Coffee, Energizing Body Butter',
    image: 'whipped-tallow-cream-coffee.png',
    link: 'https://www.etsy.com/listing/4436114326/whipped-tallow-balm-coffee',
    scentBenefits: 'Energizing, rich aroma',
    price: 21,
    category: 'warm'
  },
  blood_orange: {
    name: 'Blood Orange',
    etsyTitle: 'Whipped Tallow Balm Blood Orange',
    image: 'whipped-tallow-cream-blood-orange.png',
    link: 'https://www.etsy.com/listing/1781836429/whipped-tallow-balm-blood-orange',
    scentBenefits: 'Vibrant, revitalizing',
    price: 21,
    category: 'citrus'
  },
  eucalyptus: {
    name: 'Eucalyptus',
    etsyTitle: 'Whipped Tallow Balm Eucalyptus, Cooling',
    image: 'whipped-tallow-cream-eucalyptus.png',
    link: 'https://www.etsy.com/listing/4436131506/whipped-tallow-balm-eucalyptus-spa-day',
    scentBenefits: 'Cooling, clearing',
    price: 21,
    category: 'herbal'
  },
  pear: {
    name: 'Pear',
    etsyTitle: 'Whipped Tallow Balm Pear',
    image: 'whipped-tallow-cream-pear.png',
    link: 'https://www.etsy.com/listing/4436060936/whipped-tallow-balm-pear-fruity-body',
    scentBenefits: 'Gentle, subtly sweet',
    price: 21,
    category: 'floral'
  },
  pineapple: {
    name: 'Pineapple',
    etsyTitle: 'Whipped Tallow Balm Pineapple',
    image: 'whipped-tallow-cream-pineapple.png',
    link: 'https://www.etsy.com/listing/4436118149/whipped-tallow-balm-pineapple-tropical',
    scentBenefits: 'Tropical, brightening',
    price: 21,
    category: 'citrus'
  },
  vanilla: {
    name: 'Vanilla',
    etsyTitle: 'Whipped Tallow Balm Vanilla, Comforting',
    image: 'whipped-tallow-cream-vanilla.png',
    link: 'https://www.etsy.com/listing/4436096258/whipped-tallow-balm-bourbon-vanilla',
    scentBenefits: 'Comforting, sweet',
    price: 21,
    category: 'warm'
  },
  lavender: {
    name: 'Lavender',
    etsyTitle: 'Whipped Tallow Balm Lavender, Calming',
    image: 'whipped-tallow-cream-lavender.png',
    link: 'https://www.etsy.com/listing/1762347567/whipped-tallow-balm-lavender-calming',
    scentBenefits: 'Calming, soothing',
    price: 21,
    category: 'herbal'
  },
  bergamot: {
    name: 'Bergamot',
    etsyTitle: 'Whipped Tallow Balm Bergamot',
    image: 'whipped-tallow-cream-bergamot.png',
    link: 'https://www.etsy.com/listing/4437057816/whipped-tallow-balm-bergamot-earl-grey',
    scentBenefits: 'Uplifting, balancing',
    price: 21,
    category: 'citrus'
  },
  rosemary: {
    name: 'Rosemary',
    etsyTitle: 'Whipped Tallow Balm Rosemary',
    image: 'whipped-tallow-cream-rosemary.png',
    link: 'https://www.etsy.com/listing/4437067417/whipped-tallow-balm-rosemary-herbaceous',
    scentBenefits: 'Stimulating, clarifying',
    price: 21,
    category: 'herbal'
  },
  honey: {
    name: 'Honey',
    etsyTitle: 'Whipped Tallow Balm Honey',
    image: 'whipped-tallow-cream-honey.png',
    link: 'https://www.etsy.com/listing/4437064787/whipped-tallow-balm-honey-sweet-body',
    scentBenefits: 'Nourishing, golden',
    price: 21,
    category: 'warm'
  },
  lemongrass: {
    name: 'Lemongrass',
    etsyTitle: 'Whipped Tallow Balm Lemongrass',
    image: 'whipped-tallow-cream-lemongrass.png',
    link: 'https://www.etsy.com/listing/4437067400/whipped-tallow-balm-lemongrass-zesty',
    scentBenefits: 'Purifying, fresh',
    price: 21,
    category: 'citrus'
  },
  peach: {
    name: 'Peach',
    etsyTitle: 'Whipped Tallow Balm Peach',
    image: 'whipped-tallow-cream-peach.png',
    link: 'https://www.etsy.com/listing/4436069562/whipped-tallow-balm-peach-sweet-fruit',
    scentBenefits: 'Gentle, delicate',
    price: 21,
    category: 'floral'
  },
  unscented: {
    name: 'Unscented',
    etsyTitle: 'Whipped Tallow Balm Unscented, Pure',
    image: 'whipped-tallow-cream-unscented.png',
    link: 'https://www.etsy.com/listing/4418307760/whipped-tallow-balm-large-53oz-150g',
    scentBenefits: 'Pure, fragrance-free',
    price: 21,
    category: 'warm'
  },
  bulk: {
    name: '6-Pack Variety',
    etsyTitle: 'Whipped Tallow Balm 6-Pack',
    image: 'whipped-tallow-cream-bulk.png',
    link: 'https://www.etsy.com/listing/4437166763/bulk-beef-tallow-1kg-grass-fed-rendered',
    scentBenefits: 'Best value, gift-ready',
    price: 126,
    category: 'warm'
  }
};

// Supported languages
export const languages = [
  { code: 'en', name: 'English' },
  { code: 'fr', name: 'Francais' },
  { code: 'de', name: 'Deutsch' },
  { code: 'es', name: 'Espanol' },
  { code: 'it', name: 'Italiano' },
  { code: 'pt', name: 'Portugues' },
  { code: 'nl', name: 'Nederlands' },
  { code: 'pl', name: 'Polski' },
  { code: 'sv', name: 'Svenska' },
  { code: 'da', name: 'Dansk' },
  { code: 'fi', name: 'Suomi' },
  { code: 'el', name: 'Ellinika' },
  { code: 'cs', name: 'Cestina' },
  { code: 'ro', name: 'Romana' },
  { code: 'hu', name: 'Magyar' },
  { code: 'sk', name: 'Slovencina' },
  { code: 'bg', name: 'Balgarski' },
  { code: 'hr', name: 'Hrvatski' },
  { code: 'sl', name: 'Slovenscina' },
  { code: 'lt', name: 'Lietuviu' },
  { code: 'lv', name: 'Latviesu' },
  { code: 'et', name: 'Eesti' },
  { code: 'mt', name: 'Malti' },
  { code: 'ga', name: 'Gaeilge' }
] as const;

export type LanguageCode = typeof languages[number]['code'];
