const products = [
  {
    id: "bag-001",
    name: "经典真皮通勤托特包",
    price: 1599,
    description: "精选头层牛皮制作，大容量设计轻松收纳日常通勤所需，简约线条彰显优雅气质，是职场女性的必备之选。",
    image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=luxury%20womens%20leather%20tote%20bag%2C%20elegant%20fashion%20product%20photo%2C%20white%20background%2C%20studio%20lighting&image_size=square_hd",
    category: "托特包",
    badge: "热卖"
  },
  {
    id: "bag-002",
    name: "法式复古链条单肩包",
    price: 1299,
    description: "金属链条肩带搭配复古牛皮包身，精致小巧却兼具实用容量，约会与日常出街皆可轻松驾驭。",
    image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=womens%20chain%20shoulder%20bag%2C%20vintage%20French%20style%2C%20fashion%20product%20photo%2C%20white%20background%2C%20studio%20lighting&image_size=square_hd",
    category: "单肩包",
    badge: "新品"
  },
  {
    id: "bag-003",
    name: "轻奢菱格纹斜挎包",
    price: 899,
    description: "经典菱格纹设计搭配金色五金件，轻盈小巧的包身适合日常出行，可调节肩带满足不同搭配需求。",
    image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=womens%20quilted%20crossbody%20bag%2C%20luxury%20fashion%20product%20photo%2C%20white%20background%2C%20studio%20lighting&image_size=square_hd",
    category: "斜挎包",
    badge: "热卖"
  },
  {
    id: "bag-004",
    name: "缎面晚宴手拿包",
    price: 599,
    description: "高级缎面材质搭配精致水晶扣，优雅小巧的手拿设计，为晚宴与派对增添一抹奢华光彩。",
    image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=womens%20satin%20evening%20clutch%20bag%2C%20elegant%20fashion%20product%20photo%2C%20white%20background%2C%20studio%20lighting&image_size=square_hd",
    category: "手拿包",
    badge: "新品"
  },
  {
    id: "bag-005",
    name: "极简软皮双肩包",
    price: 1199,
    description: "柔软牛皮材质带来极致触感，极简设计搭配多功能分区收纳，适合日常通勤与短途旅行。",
    image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=womens%20leather%20backpack%2C%20minimalist%20fashion%20product%20photo%2C%20white%20background%2C%20studio%20lighting&image_size=square_hd",
    category: "双肩包"
  },
  {
    id: "bag-006",
    name: "鳄鱼纹手提饺子包",
    price: 2599,
    description: "奢华鳄鱼压纹牛皮搭配挺括包型，精致手提设计凸显高级质感，是商务场合与重要约会的点睛之选。",
    image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=luxury%20womens%20crocodile%20texture%20top%20handle%20bag%2C%20elegant%20fashion%20product%20photo%2C%20white%20background%2C%20studio%20lighting&image_size=square_hd",
    category: "手提包",
    badge: "热卖"
  },
  {
    id: "bag-007",
    name: "抽绳水桶包",
    price: 799,
    description: "率性水桶包型搭配束口抽绳设计，兼具颜值与实用性，柔软皮革与金属细节碰撞出别样时尚感。",
    image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=womens%20leather%20bucket%20bag%2C%20fashion%20product%20photo%2C%20white%20background%2C%20studio%20lighting&image_size=square_hd",
    category: "水桶包"
  },
  {
    id: "bag-008",
    name: "复古马鞍斜挎包",
    price: 299,
    description: "复古马鞍造型搭配做旧五金，小巧精致的包身承载日常小物刚刚好，文艺少女出街必备单品。",
    image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=womens%20saddle%20crossbody%20bag%2C%20vintage%20fashion%20product%20photo%2C%20white%20background%2C%20studio%20lighting&image_size=square_hd",
    category: "斜挎包"
  }
];

if (typeof module !== "undefined" && module.exports) {
  module.exports = { products };
}