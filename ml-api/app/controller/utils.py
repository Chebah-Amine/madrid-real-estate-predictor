EXPECTED_KEYS = {'sq_mt_built', 'n_rooms', 'n_bathrooms', 'floor', 'is_floor_under',
                 'rent_price', 'buy_price_by_area', 'house_type_id',
                 'is_renewal_needed', 'is_new_development', 'has_central_heating',
                 'has_individual_heating', 'has_ac', 'has_lift', 'is_exterior',
                 'has_garden', 'has_pool', 'has_terrace', 'has_storage_room',
                 'is_accessible', 'has_green_zones', 'energy_certificate', 'has_parking',
                 'is_orientation_north', 'is_orientation_west', 'is_orientation_south',
                 'is_orientation_east', 'latitude', 'longitude', 'subtitle'}

def validate_input(input_data):
    input_keys = set(input_data.keys())
    missing_keys = EXPECTED_KEYS - input_keys
    extra_keys = input_keys - EXPECTED_KEYS

    if missing_keys:
        return False, f"Missing keys: {', '.join(missing_keys)}"
    if extra_keys:
        return False, f"Extra keys not expected: {', '.join(extra_keys)}"
    return True, "Input is valid"
