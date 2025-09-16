export interface Train {
	train_id: string;
	rake_status_current: 'stabled' | 'in_service' | 'maintenance';
	violates_mandatory_fitness: boolean;
	critical_job_card_flag: boolean;
	cleaning_required: boolean;
	cleaning_slot_booked: boolean;
	readiness_probability: number;
	odometer_total_km: number;
	wear_index: number;
	branding_min_exposure_hours: number;
	branding_current_exposure_hours: number;
	shunting_moves_needed: number;
	score_components: { readiness: number; branding: number; shunting: number };
	manual_override?: {
		decision: 'Induct' | 'Hold';
		reason: string;
	};
}

export const mockTrains: Train[] = [
	{
		train_id: 'TS012',
		rake_status_current: 'stabled',
		violates_mandatory_fitness: false,
		critical_job_card_flag: false,
		cleaning_required: false,
		cleaning_slot_booked: true,
		readiness_probability: 98,
		odometer_total_km: 512345,
		wear_index: 0.42,
		branding_min_exposure_hours: 10.0,
		branding_current_exposure_hours: 6.5,
		shunting_moves_needed: 3,
		score_components: { readiness: 10.0, branding: -2.0, shunting: -1.2 }
	},
	{
		train_id: 'TS015',
		rake_status_current: 'maintenance',
		violates_mandatory_fitness: true, // This will make it "Excluded"
		critical_job_card_flag: false,
		cleaning_required: true,
		cleaning_slot_booked: true,
		readiness_probability: 0,
		odometer_total_km: 489123,
		wear_index: 0.61,
		branding_min_exposure_hours: 10.0,
		branding_current_exposure_hours: 8.1,
		shunting_moves_needed: 1,
		score_components: { readiness: -50.0, branding: -1.5, shunting: -0.5 }
	},
	{
		train_id: 'TS018',
		rake_status_current: 'stabled',
		violates_mandatory_fitness: false,
		critical_job_card_flag: true, // This will also make it "Excluded"
		cleaning_required: false,
		cleaning_slot_booked: false,
		readiness_probability: 25,
		odometer_total_km: 601458,
		wear_index: 0.75,
		branding_min_exposure_hours: 0,
		branding_current_exposure_hours: 0,
		shunting_moves_needed: 5,
		score_components: { readiness: -45.0, branding: 0, shunting: -2.5 }
	},
	{
		train_id: 'TS021',
		rake_status_current: 'stabled',
		violates_mandatory_fitness: false,
		critical_job_card_flag: false,
		cleaning_required: true,
		cleaning_slot_booked: false, // This will make it "On Hold"
		readiness_probability: 60,
		odometer_total_km: 395000,
		wear_index: 0.33,
		branding_min_exposure_hours: 0,
		branding_current_exposure_hours: 0,
		shunting_moves_needed: 2,
		score_components: { readiness: -5.0, branding: 0, shunting: -1.0 }
	}
];
