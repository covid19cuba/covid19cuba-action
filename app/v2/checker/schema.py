schema = {
    'type': 'object',
    'properties': {
        'schema-version': {
            'type': 'integer',
            'minimum': 1
        },
        'note': {
            'anyOf': [
                {
                    'type': 'string',
                },
                {
                    'type': 'null'
                }
            ]
        },
        'centros_aislamiento': {
            'type': 'object',
            'patternProperties': {
                '[\\s\\S]*': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string'
                        },
                        'nombre': {
                            'type': 'string'
                        },
                        'provincia': {
                            'type': 'string',
                            'enum': [
                                'Desconocida',
                                'La Habana',
                                'Matanzas',
                                'Cienfuegos',
                                'Sancti Spíritus',
                                'Las Tunas',
                                'Holguín',
                                'Granma',
                                'Santiago de Cuba',
                                'Isla de la Juventud',
                                'Camagüey',
                                'Ciego de Ávila',
                                'Villa Clara',
                                'Guantánamo',
                                'Pinar del Río',
                                'Artemisa',
                                'Mayabeque'
                            ]
                        },
                        'dpacode_provincia': {
                            'type': 'string',
                            'enum': [
                                '00',
                                '23',
                                '25',
                                '27',
                                '28',
                                '31',
                                '32',
                                '33',
                                '34',
                                '40.01',
                                '30',
                                '29',
                                '26',
                                '35',
                                '21',
                                '22',
                                '24'
                            ]
                        }
                    },
                    'required': [
                        'id',
                        'nombre',
                        'provincia',
                        'dpacode_provincia'
                    ]
                }
            },
            'additionalProperties': False
        },
        'centros_diagnostico': {
            'type': 'object',
            'patternProperties': {
                '[\\s\\S]*': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string'
                        },
                        'nombre': {
                            'type': 'string'
                        },
                        'provincia': {
                            'type': 'string',
                            'enum': [
                                'Desconocida',
                                'La Habana',
                                'Matanzas',
                                'Cienfuegos',
                                'Sancti Spíritus',
                                'Las Tunas',
                                'Holguín',
                                'Granma',
                                'Santiago de Cuba',
                                'Isla de la Juventud',
                                'Camagüey',
                                'Ciego de Ávila',
                                'Villa Clara',
                                'Guantánamo',
                                'Pinar del Río',
                                'Artemisa',
                                'Mayabeque'
                            ]
                        },
                        'dpacode_provincia': {
                            'type': 'string',
                            'enum': [
                                '00',
                                '23',
                                '25',
                                '27',
                                '28',
                                '31',
                                '32',
                                '33',
                                '34',
                                '40.01',
                                '30',
                                '29',
                                '26',
                                '35',
                                '21',
                                '22',
                                '24'
                            ]
                        }
                    },
                    'required': [
                        'id',
                        'nombre',
                        'provincia',
                        'dpacode_provincia'
                    ]
                }
            },
            'additionalProperties': False
        },
        'casos': {
            'type': 'object',
            'properties': {
                'dias': {
                    'type': 'object',
                    'patternProperties': {
                        '[0-9]+': {
                            'type': 'object',
                            'properties': {
                                'fecha': {
                                    'type': 'string',
                                    'pattern': '^[0-9]+/[0-9]+/[0-9]+$'
                                },
                                'diagnosticados': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {
                                                'type': 'string'
                                            },
                                            'pais': {
                                                'type': 'string'
                                            },
                                            'edad': {
                                                'anyOf': [
                                                    {
                                                        'type': 'integer',
                                                        'minimum': 1
                                                    },
                                                    {
                                                        'type': 'null'
                                                    }
                                                ]
                                            },
                                            'sexo': {
                                                'anyOf': [
                                                    {
                                                        'type': 'string',
                                                        'enum': [
                                                            'hombre',
                                                            'mujer',
                                                            'no reportado'
                                                        ]
                                                    },
                                                    {
                                                        'type': 'null'
                                                    }
                                                ]
                                            },
                                            'arribo_a_cuba_foco': {
                                                'anyOf': [
                                                    {
                                                        'type': 'string',
                                                        'pattern': '^[0-9]+/[0-9]+/[0-9]+$'
                                                    },
                                                    {
                                                        'type': 'null'
                                                    }
                                                ]
                                            },
                                            'consulta_medico': {
                                                'anyOf': [
                                                    {
                                                        'type': 'string',
                                                        'pattern': '^[0-9]+/[0-9]+/[0-9]+$'
                                                    },
                                                    {
                                                        'type': 'null'
                                                    }
                                                ]
                                            },
                                            'municipio_detección': {
                                                'anyOf': [
                                                    {
                                                        'type': 'string',
                                                        'enum': [
                                                            'Desconocido',
                                                            'Martí',
                                                            'Cárdenas',
                                                            'Habana del Este',
                                                            'Santa Cruz del Norte',
                                                            'Centro Habana',
                                                            'Regla',
                                                            'Sagua La Grande',
                                                            'Plaza de la Revolución',
                                                            'La Habana Vieja',
                                                            'Cerro',
                                                            'Diez de Octubre',
                                                            'Guanabacoa',
                                                            'San Miguel del Padrón',
                                                            'Playa',
                                                            'Arroyo Naranjo',
                                                            'Boyeros',
                                                            'Marianao',
                                                            'San José de las Lajas',
                                                            'Jaruco',
                                                            'Cotorro',
                                                            'La Lisa',
                                                            'Bauta',
                                                            'Matanzas',
                                                            'Caimito',
                                                            'Madruga',
                                                            'Limonar',
                                                            'Corralillo',
                                                            'Mariel',
                                                            'Bejucal',
                                                            'Bahía Honda',
                                                            'San Antonio de los Baños',
                                                            'Artemisa',
                                                            'Guanajay',
                                                            'Quemado de Güines',
                                                            'La Palma',
                                                            'Quivicán',
                                                            'Güines',
                                                            'Unión de Reyes',
                                                            'San Nicolás',
                                                            'Nueva Paz',
                                                            'Perico',
                                                            'Jovellanos',
                                                            'Alquízar',
                                                            'Pedro Betancourt',
                                                            'Güira de Melena',
                                                            'Candelaria',
                                                            'Batabanó',
                                                            'Los Arabos',
                                                            'Melena del Sur',
                                                            'Colón',
                                                            'Viñales',
                                                            'San Cristóbal',
                                                            'Santo Domingo',
                                                            'Cifuentes',
                                                            'Jagüey Grande',
                                                            'Los Palacios',
                                                            'Calimete',
                                                            'Minas de Matahambre',
                                                            'Consolación del Sur',
                                                            'Mantua',
                                                            'Rodas',
                                                            'Ranchuelo',
                                                            'Lajas',
                                                            'Cienaga de Zapata',
                                                            'Santa Clara',
                                                            'Pinar del Río',
                                                            'Aguada de Pasajeros',
                                                            'Manicaragua',
                                                            'San Juan y Martínez',
                                                            'Guane',
                                                            'Palmira',
                                                            'Cruces',
                                                            'Cumanayagua',
                                                            'Cienfuegos',
                                                            'Abreus',
                                                            'San Luis',
                                                            'Sandino',
                                                            'Isla de la Juventud',
                                                            'Trinidad',
                                                            'Encrucijada',
                                                            'Chambas',
                                                            'Camajuaní',
                                                            'Caibarién',
                                                            'Yaguajay',
                                                            'Nuevitas',
                                                            'Remedios',
                                                            'Placetas',
                                                            'Morón',
                                                            'Cabaiguán',
                                                            'Fomento',
                                                            'Taguasco',
                                                            'Florencia',
                                                            'Jatibonico',
                                                            'Ciro Redondo',
                                                            'Bolivia',
                                                            'Primero de Enero',
                                                            'Sancti Spíritus',
                                                            'Majagua',
                                                            'Esmeralda',
                                                            'Ciego de Ávila',
                                                            'Sierra de Cubitas',
                                                            'Baraguá',
                                                            'Venezuela',
                                                            'Minas',
                                                            'Carlos Manuel de Céspedes',
                                                            'La Sierpe',
                                                            'Florida',
                                                            'Camagüey',
                                                            'Guáimaro',
                                                            'Sibanicú',
                                                            'Manatí',
                                                            'Vertientes',
                                                            'Jimaguayú',
                                                            'Jesús Menéndez',
                                                            'Puerto Padre',
                                                            'Banes',
                                                            'Santa Cruz del Sur',
                                                            'Gibara',
                                                            'Najasa',
                                                            'Rafael Freyre',
                                                            'Las Tunas',
                                                            'Calixto García',
                                                            'Holguín',
                                                            'Jobabo',
                                                            'Colombia',
                                                            'Amancio',
                                                            'Majibacoa',
                                                            'Báguanos',
                                                            'Antilla',
                                                            'Mayarí',
                                                            'Cacocum',
                                                            'Río Cauto',
                                                            'Moa',
                                                            'Cauto Cristo',
                                                            'Frank País',
                                                            'Cueto',
                                                            'Urbano Noris',
                                                            'Sagua de Tánamo',
                                                            'Segundo Frente',
                                                            'Bayamo',
                                                            'Jiguaní',
                                                            'Guantánamo',
                                                            'Mella',
                                                            'Yateras',
                                                            'Contramaestre',
                                                            'Yara',
                                                            'San Luis',
                                                            'Palma Soriano',
                                                            'El Salvador',
                                                            'Manzanillo',
                                                            'Songo La Maya',
                                                            'Guisa',
                                                            'Tercer Frente',
                                                            'Buey Arriba',
                                                            'Manuel Tames',
                                                            'Bartolomé Masó',
                                                            'Niceto Pérez',
                                                            'Media Luna',
                                                            'Santiago de Cuba',
                                                            'Guamá',
                                                            'Caimanera',
                                                            'San Antonio del Sur',
                                                            'Niquero',
                                                            'Pilón',
                                                            'Baracoa',
                                                            'Imías',
                                                            'Maisí',
                                                            'Campechuela'
                                                        ]
                                                    },
                                                    {
                                                        'type': 'null'
                                                    }
                                                ]
                                            },
                                            'provincia_detección': {
                                                'anyOf': [
                                                    {
                                                        'type': 'string',
                                                        'enum': [
                                                            'Desconocida',
                                                            'La Habana',
                                                            'Matanzas',
                                                            'Cienfuegos',
                                                            'Sancti Spíritus',
                                                            'Las Tunas',
                                                            'Holguín',
                                                            'Granma',
                                                            'Santiago de Cuba',
                                                            'Isla de la Juventud',
                                                            'Camagüey',
                                                            'Ciego de Ávila',
                                                            'Villa Clara',
                                                            'Guantánamo',
                                                            'Pinar del Río',
                                                            'Artemisa',
                                                            'Mayabeque'
                                                        ]
                                                    },
                                                    {
                                                        'type': 'null'
                                                    }
                                                ]
                                            },
                                            'dpacode_municipio_deteccion': {
                                                'anyOf': [
                                                    {
                                                        'type': 'string',
                                                        'enum': [
                                                            '00.00',
                                                            '25.03',
                                                            '25.02',
                                                            '23.06',
                                                            '24.04',
                                                            '23.03',
                                                            '23.05',
                                                            '26.03',
                                                            '23.02',
                                                            '23.04',
                                                            '23.10',
                                                            '23.09',
                                                            '23.07',
                                                            '23.08',
                                                            '23.01',
                                                            '23.14',
                                                            '23.13',
                                                            '23.11',
                                                            '24.02',
                                                            '24.03',
                                                            '23.15',
                                                            '23.12',
                                                            '22.05',
                                                            '25.01',
                                                            '22.04',
                                                            '24.05',
                                                            '25.08',
                                                            '26.01',
                                                            '22.02',
                                                            '24.01',
                                                            '22.01',
                                                            '22.06',
                                                            '22.09',
                                                            '22.03',
                                                            '26.02',
                                                            '21.05',
                                                            '24.11',
                                                            '24.08',
                                                            '25.09',
                                                            '24.07',
                                                            '24.06',
                                                            '25.05',
                                                            '25.06',
                                                            '22.08',
                                                            '25.07',
                                                            '22.07',
                                                            '22.10',
                                                            '24.10',
                                                            '25.13',
                                                            '24.09',
                                                            '25.04',
                                                            '21.04',
                                                            '22.11',
                                                            '26.11',
                                                            '26.10',
                                                            '25.11',
                                                            '21.06',
                                                            '25.12',
                                                            '21.03',
                                                            '21.07',
                                                            '21.02',
                                                            '27.02',
                                                            '26.12',
                                                            '27.04',
                                                            '25.10',
                                                            '26.09',
                                                            '21.08',
                                                            '27.01',
                                                            '26.13',
                                                            '21.10',
                                                            '21.11',
                                                            '27.03',
                                                            '27.05',
                                                            '27.06',
                                                            '27.07',
                                                            '27.08',
                                                            '21.09',
                                                            '21.01',
                                                            '40.01',
                                                            '28.06',
                                                            '26.04',
                                                            '29.01',
                                                            '26.05',
                                                            '26.06',
                                                            '28.01',
                                                            '30.05',
                                                            '26.07',
                                                            '26.08',
                                                            '29.02',
                                                            '28.04',
                                                            '28.05',
                                                            '28.03',
                                                            '29.06',
                                                            '28.02',
                                                            '29.05',
                                                            '29.03',
                                                            '29.04',
                                                            '28.07',
                                                            '29.07',
                                                            '30.02',
                                                            '29.08',
                                                            '30.03',
                                                            '29.10',
                                                            '29.09',
                                                            '30.04',
                                                            '30.01',
                                                            '28.08',
                                                            '30.09',
                                                            '30.08',
                                                            '30.06',
                                                            '30.07',
                                                            '31.01',
                                                            '30.10',
                                                            '30.11',
                                                            '31.03',
                                                            '31.02',
                                                            '32.03',
                                                            '30.13',
                                                            '32.01',
                                                            '30.12',
                                                            '32.02',
                                                            '31.05',
                                                            '32.07',
                                                            '32.06',
                                                            '31.06',
                                                            '31.07',
                                                            '31.08',
                                                            '31.04',
                                                            '32.05',
                                                            '32.04',
                                                            '32.11',
                                                            '32.08',
                                                            '33.01',
                                                            '32.14',
                                                            '33.02',
                                                            '32.12',
                                                            '32.10',
                                                            '32.09',
                                                            '32.13',
                                                            '34.04',
                                                            '33.04',
                                                            '33.03',
                                                            '35.09',
                                                            '34.02',
                                                            '35.03',
                                                            '34.01',
                                                            '33.05',
                                                            '34.03',
                                                            '34.07',
                                                            '35.01',
                                                            '33.06',
                                                            '34.05',
                                                            '33.13',
                                                            '34.08',
                                                            '33.12',
                                                            '35.02',
                                                            '33.11',
                                                            '35.10',
                                                            '33.08',
                                                            '34.06',
                                                            '34.09',
                                                            '35.08',
                                                            '35.07',
                                                            '33.09',
                                                            '33.10',
                                                            '35.04',
                                                            '35.06',
                                                            '35.05',
                                                            '33.07'
                                                        ]
                                                    },
                                                    {
                                                        'type': 'null'
                                                    }
                                                ]
                                            },
                                            'dpacode_provincia_deteccion': {
                                                'anyOf': [
                                                    {
                                                        'type': 'string',
                                                        'enum': [
                                                            '00',
                                                            '23',
                                                            '25',
                                                            '27',
                                                            '28',
                                                            '31',
                                                            '32',
                                                            '33',
                                                            '34',
                                                            '40.01',
                                                            '30',
                                                            '29',
                                                            '26',
                                                            '35',
                                                            '21',
                                                            '22',
                                                            '24'
                                                        ]
                                                    },
                                                    {
                                                        'type': 'null'
                                                    }
                                                ]
                                            },
                                            'contagio': {
                                                'anyOf': [
                                                    {
                                                        'type': 'string',
                                                        'enum': [
                                                            'importado',
                                                            'introducido',
                                                            'autoctono',
                                                            'desconocido'
                                                        ]
                                                    },
                                                    {
                                                        'type': 'null'
                                                    }
                                                ]
                                            },
                                            'contacto_focal': {
                                                'anyOf': [
                                                    {
                                                        'type': 'integer',
                                                        'minimum': 0
                                                    },
                                                    {
                                                        'type': 'null'
                                                    }
                                                ]
                                            },
                                            'centro_aislamiento': {
                                                'anyOf': [
                                                    {
                                                        'type': 'string'
                                                    },
                                                    {
                                                        'type': 'null'
                                                    }
                                                ]
                                            },
                                            'centro_diagnostico': {
                                                'anyOf': [
                                                    {
                                                        'type': 'string'
                                                    },
                                                    {
                                                        'type': 'null'
                                                    }
                                                ]
                                            },
                                            'posible_procedencia_contagio': {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'string'
                                                }
                                            },
                                            'provincias_visitadas': {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'string'
                                                }
                                            },
                                            'dpacode_provincias_visitadas': {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'string'
                                                }
                                            }
                                        }
                                    }
                                },
                                'sujetos_riesgo': {
                                    'type': 'integer',
                                    'minimum': 0
                                },
                                'graves_numero': {
                                    'type': 'integer',
                                    'minimum': 0
                                },
                                'criticos_numero': {
                                    'type': 'integer',
                                    'minimum': 0
                                },
                                'graves_id': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'string'
                                    }
                                },
                                'muertes_numero': {
                                    'type': 'integer',
                                    'minimum': 0
                                },
                                'muertes_id': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'string'
                                    }
                                },
                                'evacuados_numero': {
                                    'type': 'integer',
                                    'minimum': 0
                                },
                                'evacuados_id': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'string'
                                    }
                                },
                                'recuperados_numero': {
                                    'type': 'integer',
                                    'minimum': 0
                                },
                                'recuperados_id': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'string'
                                    }
                                },
                                'tests_total': {
                                    'type': 'integer',
                                    'minimum': 0
                                }
                            }
                        }
                    },
                    'additionalProperties': False
                }
            },
            'required': [
                'dias'
            ]
        }
    },
    'required': [
        'centros_aislamiento',
        'centros_diagnostico',
        'casos'
    ]
}
