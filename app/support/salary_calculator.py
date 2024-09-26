from typing import Optional


class UFOProfileConverter:
    def convert_to_salary_scale(ufo_profile: str):
        ufo_to_scale = {
            'ICT Ontwikkelaar 1': 'Scale 12',
            'ICT Ontwikkelaar 2': 'Scale 11',
            'ICT Ontwikkelaar 3': 'Scale 10',
            'ICT Ontwikkelaar 4': 'Scale 9',
            'ICT Ontwikkelaar 5': 'Scale 8',
            'ICT Developer 1': 'Scale 12',
            'ICT Developer 2': 'Scale 11',
            'ICT Developer 3': 'Scale 10',
            'ICT Developer 4': 'Scale 9',
            'ICT Developer 5': 'Scale 8',
            'ICT Consultant 1': 'Scale 12',
            'ICT Consultant 2': 'Scale 11',
            'ICT Consultant 3': 'Scale 10',
            'ICT Manager 1': 'Scale 11',
            'ICT Manager 2': 'Scale 10',
            'ICT Manager 3': 'Scale 9',
            'ICT Manager 4': 'Scale 8',
            'ICT Manager 5': 'Scale 7',
            'Head of Department 1': 'Scale 13',
            'Head of Department 2': 'Scale 12',
            'Head of Department 3': 'Scale 11',
            'Managing Director 1': 'Scale 14',
            'Managing Director 2': 'Scale 13',
            'Managing Director 3': 'Scale 12',
            'Managing Director 4': 'Scale 11',
        }

        if ufo_profile not in ufo_to_scale:
            return 'Unable to convert given UFO profile to salary scale.'
        else:
            return ufo_to_scale[ufo_profile]

    def convert_salary_scale_to_salary_range(salary_scale: str):
        scale_to_salary_range = {
            'Scale 1': '€2618 – €2618',
            'Scale 2': '€2618 – €2618',
            'Scale 3': '€2618 – €2846',
            'Scale 4': '€2618 – €2995',
            'Scale 5': '€2618 – €3149',
            'Scale 6': '€2618 – €3298',
            'Scale 7': '€2693 – €3636',
            'Scale 8': '€3027 – €4103',
            'Scale 9': '€3377 – €4640',
            'Scale 10': '€3226 – €5090',
            'Scale 11': '€4332 – €5929',
            'Scale 12': '€5247 – €6737',
            'Scale 13': '€6002 – €7305',
            'Scale 14': '€6305 – €8025',
            'Scale 15': '€6836 – €8815',
            'Scale 16': '€7405 – €9680',
            'Scale 17': '€8025 – €10635',
            'Scale 18': '€8815 – €11686',
        }

        if salary_scale not in scale_to_salary_range:
            return 'Unable to convert given Salary Scale to salary range.'
        else:
            return scale_to_salary_range[salary_scale]
