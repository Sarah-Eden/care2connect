from datetime import timedelta


# All Schedule values = age in months
EPSDT_REQUIREMENTS = {
	'well_child_schedule': {
		'display_name': 'Well Child Checkup',
		'age_in_months': [1, 2, 4, 6, 9, 12, 15, 18, 24, 30, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144, 156, 168, 180, 192, 204, 216] 
	},

	'immunization_schedule': {
		'HepB': {
			'display_name': 'Hepatitis B',
			'total_doses': 3,
			'schedule': [
				{'age_months': 0, 'dose': '1st'},
				{'age_months': [1, 2], 'dose': '2nd'},
				{'age_months': [6, 9, 12, 15, 18], 'dose': '3rd'}
			]},
		
		'RV1': {
			'display_name': 'Rotavirus (RV1)',
			'total_doses': 2,
			'schedule': [
				{'age_months': 2, 'dose': '1st'},
				{'age_months': 4, 'dose': '2nd'}
			]},

		'RV5': {
			'display_name': 'Rotavirus (RV5)',
			'total_doses': 3,
			'schedule': [
				{'age_months': 2, 'dose': '1st'},
				{'age_months': 4, 'dose': '2nd'},
				{'age_months': 6, 'dose': '3rd'}
			]},

		# Only for patients < 7 years of age
		'DTaP': {
			'display_name': 'Diphtheria, tetanus, acellular pertussis',
			'total_doses': 5,
			'schedule': [
				{'age_months': 2, 'dose': '1st'},
				{'age_months': 4, 'dose': '2nd'},
				{'age_months': 6, 'dose': '3rd'},
				{'age_months': [12, 15], 'dose': '4th'},
				{'age_months': [48, 60, 72], 'dose': '5th'}
			]},

		# Only for patients > 7 years of age
		'Tdap': {
			'display_name': 'Tetanus, diphtheria, acellular pertussis',
			'total_doses': 1,
			'schedule': [
				{'age_months': [132, 144], 'dose': '1st'}
			]},

		'Hib': {
			'display_name': 'Haemophilus influenzae type b',
			'total_doses': 4,
			'schedule': [
				{'age_months': 2, 'dose': '1st'},
				{'age_months': 4, 'dose': '2nd'},
				{'age_months': 6, 'dose': '3rd'},
				{'age_months': [12, 15], 'dose': '4th'}
			]}, 

		'PCV15': {
			'display_name': 'Pneumococcal polysaccharide vaccine (PCV15)',
			'total_doses': 4,
			'schedule': [
				{'age_months': 2, 'dose': '1st'},
				{'age_months': 4, 'dose': '2nd'},
				{'age_months': 6, 'dose': '3rd'},
				{'age_months': [12, 15], 'dose': '4th'}
			]},

		'PCV20': {
			'display_name': 'Pneumococcal polysaccharide vaccine (PCV20)',
			'total_doses': 4,
			'schedule': [
				{'age_months': 2, 'dose': '1st'},
				{'age_months': 4, 'dose': '2nd'},
				{'age_months': 6, 'dose': '3rd'},
				{'age_months': [12, 15], 'dose': '4th'}
			]},

		'IPV': {
			'display_name': 'Inactivated poliovirus (IPV)',
			'total_doses': 4,
			'schedule': [
				{'age_months': 2, 'dose': '1st'},
				{'age_months': 4, 'dose': '2nd'},
				{'age_months': [6, 9, 12, 15, 18], 'dose': '3rd'},
				{'age_months': [48, 60, 72], 'dose': '4th'}
			]}, 

		'MMR': {
			'display_name': 'Measles, mumps, rubella (MMR)',
			'total_doses': 2,
			'schedule':[
				{'age_months': [12, 15], 'dose': '1st'},
				{'age_months': [48, 60, 72], 'dose': '2nd'}
			]},

		'VAR': {
			'display_name': 'Varicella (VAR)',
			'total_doses': 2,
			'schedule': [
				{'age_months': [12, 15], 'dose': '1st'},
				{'age_months': [48, 60, 72], 'dose': '2nd'}
		]}, 

		'HepA': {
			'display_name': 'Hepatitis A (HepA)',
			'total_doses': 2,
			'schedule': [
				{'age_months': 12, 'dose': '1st'},
				{'age_months': 18, 'dose': '2nd'}
		]},

		'HPV': {
			'display_name': 'Human papillomavirus (HPV)',
			'total_doses': 2,
			'schedule': [
				{'age_months': 108, 'dose': '1st'},
				{'age_months': 120, 'dose': '2nd'}
		]}, 

		'MenACWY-TT': {
			'display_name': 'Meningococcal (MenACWY-TT)',
			'total_doses': 2,
			'schedule': [
				{'age_months': [132, 144], 'dose': '1st'},
				{'age_months': 192, 'dose': '2nd'}
		]}, 

		'IIV3': {
			'display_name': 'Influenza (IIV3)',
			'total_doses': 0,
			'schedule': [
				{'first_age': 12},
				{'interval_after_first': timedelta(days=365.25)}
		]},

		# Optional Vaccine, no current recommended schedule
		'COVID_mRNA': {
			'display_name': 'COVID-19 (1vCOV-mRNA)',
			'total_doses': 0
		},

		# Optional Vaccine, no current recommended schedule
		'COVID_aPS': {
			'display_name': 'COVID-19 (1vCOV-aPS)',
			'total_doses': 0
		},
		'None': {
			'display_name': 'None',
			'total_doses': 0
		} 
	},

	'dental': {
		'display_name': 'Dental Cleaning',
		'schedule': [
			{'first_age': 12},
			{'interval_after_first': timedelta(days=183)}
	]}
}

SERVICE_CHOICES = (
		('well_child', 'Well Child Checkup'),
		('immunization(s)', 'Immunization(s)'),
		('dental', 'Dental Cleaning')
	)

IMMUNIZATION_CHOICES = tuple((vaccine, data['display_name']) for vaccine, data in EPSDT_REQUIREMENTS['immunization_schedule'].items())
IMMUNIZATION_DOSES = { vaccine: data['total_doses'] for vaccine, data in EPSDT_REQUIREMENTS['immunization_schedule'].items()}