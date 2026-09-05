/** Single source of truth for firm details repeated across the site. */
export const FIRM = {
  name: "Winters & Yonker, P.A.",
  tagline: "The Aggressive Attorneys",
  phone: "(813) 223-6200",
  phoneHref: "8132236200",
  /** NOTE: conflicts with "115+" on the live About page — confirm before launch. */
  yearsCombined: "119+",
  attorneyCount: 10,
  reviewScore: "4.9",
  reviewCount: "1,100+",
} as const;

export const OFFICES = [
  { city: "Tampa", street: "601 W Swann Ave", zip: "33606" },
  { city: "Clearwater", street: "1006 Drew St", zip: "33755" },
  { city: "St. Petersburg", street: "111 2nd Ave NE, Ste 350", zip: "33701" },
  { city: "New Port Richey", street: "5006 Trouble Creek Rd #200", zip: "34652" },
  { city: "Lakeland", street: "1543 Lakeland Hills Blvd, Ste 18", zip: "33805" },
] as const;

export const COUNTIES = [
  { name: "Hillsborough", towns: ["Tampa", "Brandon", "Riverview", "Plant City", "Temple Terrace", "Valrico", "Ruskin", "Apollo Beach"] },
  { name: "Pinellas", towns: ["St. Petersburg", "Clearwater", "Largo", "Pinellas Park", "Palm Harbor", "Dunedin", "Seminole"] },
  { name: "Pasco", towns: ["New Port Richey", "Port Richey", "Wesley Chapel", "Land O' Lakes", "Hudson", "Zephyrhills"] },
  { name: "Polk", towns: ["Lakeland", "Winter Haven", "Bartow", "Auburndale", "Haines City", "Davenport"] },
] as const;
