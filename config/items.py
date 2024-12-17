ITEMS = {
    1: {
        'name': 'Энергетик',
        'description': 'Восстанавливает 5 энергии',
        'type': 'consumable',
        'price': 100,
        'effect': {'energy': 5}
    },
    2: {
        'name': 'Бустер опыта',
        'description': 'Удваивает получаемый опыт на 1 час',
        'type': 'boost',
        'price': 500,
        'duration': 3600
    },
    3: {
        'name': 'Бустер майнинга',
        'description': 'Увеличивает добычу на 2 часа',
        'type': 'boost',
        'price': 750,
        'duration': 7200
    },
    4: {
        'name': 'Улучшение майнинга',
        'description': 'Увеличивает силу майнинга на 1',
        'type': 'upgrade',
        'price': 1000,
        'effect': {'mining_power': 1}
    }
}

SHOP_ITEMS = {
    1: {
        'name': 'Энергетик',
        'price': 100,
        'description': 'Восстанавливает 5 энергии'
    },
    2: {
        'name': 'Бустер опыта',
        'price': 500,
        'description': 'Удваивает получаемый опыт на 1 час'
    },
    3: {
        'name': 'Бустер майнинга',
        'price': 750,
        'description': 'Увеличивает добычу на 2 часа'
    }
}
