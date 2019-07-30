"""
.. module:: Init data
   :platform: Unix, Windows
   :synopsis: Some data is required to run Deployment Manager for the first time.
       This file has all the necessary data required to run Deployment Manager.
       Each List variable below is Data in key-value format and is populated in respective collection by InitDataHelper.py when the application comes up.
.. moduleauthor:: name <email@amdocs.com>

"""

# Reports to be populated for GUI Reference
reports = [{
    "name": "DU_Deployed_On_Multiple_Machine",
    "url": "http://hostname:8085/files/workspace.html#/DPM/DeploymentManager/Reports/DU_Deployed_On_Multiple_Machine.slam/view",
    "collection_name": "Reports.DU_Deployed_On_Multiple_Machine\.slam.index"
},
    {
    "name": "Successful_Tool_Deployments",
    "url": "http://hostname:8085/files/workspace.html#/DPM/DeploymentManager/Reports/Successful_Tool_Deployments.slam/view",
    "collection_name": "Reports.Successful_Tool_Deployments\.slam.index"
},
    {
    "name": "Successful_DU_Deployments",
    "url": "http://hostname:8085/files/workspace.html#/DPM/DeploymentManager/Reports/Successful_DU_Deployments.slam/view",
    "collection_name": "Reports.Successful_DU_Deployments\.slam.index"
},
    {
    "name": "Tool_Deployed_On_Multiple_Machines",
    "url": "http://hostname:8085/files/workspace.html#/DPM/DeploymentManager/Reports/Tool_Deployed_On_Multiple_Machines.slam/view",
    "collection_name": "Reports.Tool_Deployed_On_Multiple_Machines\.slam.index"
},
    {
    "name": "Multiple_Tools_Deployed_On_Machine",
    "url": "http://hostname:8085/files/workspace.html#/DPM/DeploymentManager/Reports/Multiple_Tools_Deployed_On_Machine.slam/view",
    "collection_name": "Reports.Multiple_Tools_Deployed_On_Machine\.slam.index"
},
    {
    "name": "DU_Deployed_History",
    "url": "http://hostname:8085/files/workspace.html#/DPM/DeploymentManager/Reports/DU_Deployment_History.slam/view",
    "collection_name": "Reports.DU_Deployment_History\.slam.index"
},
    {
    "name": "Tool_Deployment_History",
    "url": "http://hostname:8085/files/workspace.html#/DPM/DeploymentManager/Reports/Tool_Deployment_History.slam/view",
    "collection_name": "Reports.Tool_Deployment_History\.slam.index"
},
    {
    "name": "Multiple_Dus_Deployed_On_Machine",
    "url": "http://hostname:8085/files/workspace.html#/DPM/DeploymentManager/Reports/Multiple_Dus_Deployed_On_Machine.slam/view",
    "collection_name": "Reports.Multiple_Dus_Deployed_On_Machine\.slam.index"
},
    {
    "name": "DUPackage_Multi_State_View",
    "url": "http://hostname:8085/files/workspace.html#/DPM/DeploymentManager/Reports/DUPackage_Multi_State_View.slam/view",
    "collection_name": "Reports.DUPackage_Multi_State_View\.slam.index"
}

]


# Definition of each report is provided below in JSONs

reports_data = [
    {"collection_name": "Reports.DU_Deployed_On_Multiple_Machine\.slam.index",
     "decks": {
         "086a06de-49e7-4eb3-a614-a667e77abc47": {
             "cards": [
                 "77bbb3a3-ad76-4814-9762-06623b8fb54c"
             ],
             "name": ""
         },
         "361b9fe5-ca68-4a38-8052-b9b0165de00d": {
             "cards": [
                 "3e3a7a4f-6916-497f-b31e-3075ac53d4b4",
                 "8d9deccd-5d8b-44ce-806b-7a3d477c646f",
                 "a8c1db7f-807a-4d35-aa21-b815435544d0",
                 "2f0d00f6-246a-47d4-af10-cf0ab4b8a4e5"
             ],
             "name": ""
         },
         "55ac4975-6602-45ee-b4d8-ccf2aa6d2d65": {
             "cards": [
                 "3e3a7a4f-6916-497f-b31e-3075ac53d4b4",
                 "8d9deccd-5d8b-44ce-806b-7a3d477c646f"
             ],
             "name": ""
         }
     },
        "cards": {
         "2f0d00f6-246a-47d4-af10-cf0ab4b8a4e5": {
             "model": {
                 "pageSize": None,
                 "page": None
             },
             "cardType": "table"
         },
         "3e3a7a4f-6916-497f-b31e-3075ac53d4b4": {
             "model": {
                 "ranges": [],
                 "text": "# Select the DeploymentUnit to find DU deployed on Multiple Machines\n\nEntities = {!`` select name from `/DPM/DeploymentManager/DeploymentUnit` order by name ``} (all)\n\n\nbeginDate = ____-__-__(2016-01-01)\n\n\nendDate = ____-__-__(2050-01-01)"
             },
             "cardType": "ace-markdown"
         },
         "77bbb3a3-ad76-4814-9762-06623b8fb54c": {
             "model": {
                 "layout": {
                     "panes": [
                         {
                             "pane": {
                                 "panes": [
                                     {
                                         "pane": {
                                             "value": "55ac4975-6602-45ee-b4d8-ccf2aa6d2d65",
                                             "type": "cell"
                                         },
                                         "ratio": [
                                             1,
                                             1
                                         ]
                                     }
                                 ],
                                 "orientation": "horizontal",
                                 "type": "split"
                             },
                             "ratio": [
                                 1,
                                 2
                             ]
                         },
                         {
                             "pane": {
                                 "panes": [
                                     {
                                         "pane": {
                                             "value": "361b9fe5-ca68-4a38-8052-b9b0165de00d",
                                             "type": "cell"
                                         },
                                         "ratio": [
                                             1,
                                             1
                                         ]
                                     }
                                 ],
                                 "orientation": "horizontal",
                                 "type": "split"
                             },
                             "ratio": [
                                 1,
                                 2
                             ]
                         }
                     ],
                     "orientation": "vertical",
                     "type": "split"
                 }
             },
             "cardType": "draftboard"
         },
         "8d9deccd-5d8b-44ce-806b-7a3d477c646f": {
             "model": {
                 "state": {
                     "Entities": {
                         "labels": {
                             "value": [
                                 {
                                     "literal": "all"
                                 },
                                 {
                                     "literal": "Abhinavtest"
                                 },
                                 {
                                     "literal": "DASAS"
                                 },
                                 {
                                     "literal": "DD"
                                 },
                                 {
                                     "literal": "DDDD"
                                 },
                                 {
                                     "literal": "DU"
                                 },
                                 {
                                     "literal": "DU1"
                                 },
                                 {
                                     "literal": "DU2"
                                 },
                                 {
                                     "literal": "DU3"
                                 },
                                 {
                                     "literal": "DU4"
                                 },
                                 {
                                     "literal": "DUsahil"
                                 },
                                 {
                                     "literal": "Latest DU"
                                 },
                                 {
                                     "literal": "No1 DU"
                                 },
                                 {
                                     "literal": "RK DU"
                                 },
                                 {
                                     "literal": "TEST"
                                 },
                                 {
                                     "literal": "Test Dubld"
                                 },
                                 {
                                     "literal": "Test1 Dubld"
                                 },
                                 {
                                     "literal": "cxsa"
                                 },
                                 {
                                     "literal": "du5"
                                 },
                                 {
                                     "literal": "du6"
                                 },
                                 {
                                     "literal": "du7"
                                 },
                                 {
                                     "literal": "du8"
                                 },
                                 {
                                     "literal": "leon2uydry"
                                 },
                                 {
                                     "literal": "recomtel"
                                 },
                                 {
                                     "literal": "saat"
                                 },
                                 {
                                     "literal": "t2"
                                 },
                                 {
                                     "literal": "testSahil"
                                 },
                                 {
                                     "literal": "usageDU"
                                 },
                                 {
                                     "literal": "yoeldu1"
                                 },
                                 {
                                     "literal": "yoeldu2"
                                 }
                             ],
                             "type": "lit"
                         },
                         "selection": {
                             "value": {
                                 "literal": "Abhinavtest"
                             },
                             "type": "lit"
                         },
                         "type": "dropdown"
                     },
                     "beginDate": {
                         "textBox": {
                             "value": {
                                 "value": {
                                     "day": 1,
                                     "month": 1,
                                     "year": 2016
                                 },
                                 "type": "lit"
                             },
                             "type": "date"
                         },
                         "type": "textbox"
                     },
                     "endDate": {
                         "textBox": {
                             "value": {
                                 "value": {
                                     "day": 1,
                                     "month": 1,
                                     "year": 2050
                                 },
                                 "type": "lit"
                             },
                             "type": "date"
                         },
                         "type": "textbox"
                     }
                 },
                 "input": {
                     "blocks": [
                         {
                             "content": [
                                 {
                                     "value": "Select",
                                     "type": "str"
                                 },
                                 {
                                     "type": "space"
                                 },
                                 {
                                     "value": "the",
                                     "type": "str"
                                 },
                                 {
                                     "type": "space"
                                 },
                                 {
                                     "value": "DeploymentUnit",
                                     "type": "str"
                                 },
                                 {
                                     "type": "space"
                                 },
                                 {
                                     "value": "to",
                                     "type": "str"
                                 },
                                 {
                                     "type": "space"
                                 },
                                 {
                                     "value": "find",
                                     "type": "str"
                                 },
                                 {
                                     "type": "space"
                                 },
                                 {
                                     "value": "DU",
                                     "type": "str"
                                 },
                                 {
                                     "type": "space"
                                 },
                                 {
                                     "value": "deployed",
                                     "type": "str"
                                 },
                                 {
                                     "type": "space"
                                 },
                                 {
                                     "value": "on",
                                     "type": "str"
                                 },
                                 {
                                     "type": "space"
                                 },
                                 {
                                     "value": "Multiple",
                                     "type": "str"
                                 },
                                 {
                                     "type": "space"
                                 },
                                 {
                                     "value": "Machines",
                                     "type": "str"
                                 }
                             ],
                             "level": 1,
                             "type": "header"
                         },
                         {
                             "content": [
                                 {
                                     "field": {
                                         "labels": {
                                             "value": [
                                                 {
                                                     "literal": "all"
                                                 },
                                                 {
                                                     "literal": "Abhinavtest"
                                                 },
                                                 {
                                                     "literal": "DASAS"
                                                 },
                                                 {
                                                     "literal": "DD"
                                                 },
                                                 {
                                                     "literal": "DDDD"
                                                 },
                                                 {
                                                     "literal": "DU"
                                                 },
                                                 {
                                                     "literal": "DU1"
                                                 },
                                                 {
                                                     "literal": "DU2"
                                                 },
                                                 {
                                                     "literal": "DU3"
                                                 },
                                                 {
                                                     "literal": "DU4"
                                                 },
                                                 {
                                                     "literal": "DUsahil"
                                                 },
                                                 {
                                                     "literal": "Latest DU"
                                                 },
                                                 {
                                                     "literal": "No1 DU"
                                                 },
                                                 {
                                                     "literal": "RK DU"
                                                 },
                                                 {
                                                     "literal": "TEST"
                                                 },
                                                 {
                                                     "literal": "Test Dubld"
                                                 },
                                                 {
                                                     "literal": "Test1 Dubld"
                                                 },
                                                 {
                                                     "literal": "cxsa"
                                                 },
                                                 {
                                                     "literal": "du5"
                                                 },
                                                 {
                                                     "literal": "du6"
                                                 },
                                                 {
                                                     "literal": "du7"
                                                 },
                                                 {
                                                     "literal": "du8"
                                                 },
                                                 {
                                                     "literal": "leon2uydry"
                                                 },
                                                 {
                                                     "literal": "recomtel"
                                                 },
                                                 {
                                                     "literal": "saat"
                                                 },
                                                 {
                                                     "literal": "t2"
                                                 },
                                                 {
                                                     "literal": "testSahil"
                                                 },
                                                 {
                                                     "literal": "usageDU"
                                                 },
                                                 {
                                                     "literal": "yoeldu1"
                                                 },
                                                 {
                                                     "literal": "yoeldu2"
                                                 }
                                             ],
                                             "type": "lit"
                                         },
                                         "selection": {
                                             "value": {
                                                 "literal": "all"
                                             },
                                             "type": "lit"
                                         },
                                         "type": "dropdown"
                                     },
                                     "required": False,
                                     "label": "Entities",
                                     "type": "field"
                                 }
                             ],
                             "type": "para"
                         },
                         {
                             "content": [
                                 {
                                     "field": {
                                         "textBox": {
                                             "value": {
                                                 "value": {
                                                     "day": 1,
                                                     "month": 1,
                                                     "year": 2016
                                                 },
                                                 "type": "lit"
                                             },
                                             "type": "date"
                                         },
                                         "type": "textbox"
                                     },
                                     "required": False,
                                     "label": "beginDate",
                                     "type": "field"
                                 }
                             ],
                             "type": "para"
                         },
                         {
                             "content": [
                                 {
                                     "field": {
                                         "textBox": {
                                             "value": {
                                                 "value": {
                                                     "day": 1,
                                                     "month": 1,
                                                     "year": 2050
                                                 },
                                                 "type": "lit"
                                             },
                                             "type": "date"
                                         },
                                         "type": "textbox"
                                     },
                                     "required": False,
                                     "label": "endDate",
                                     "type": "field"
                                 }
                             ],
                             "type": "para"
                         }
                     ],
                     "doc": "slamdown"
                 }
             },
             "cardType": "markdown"
         },
         "a8c1db7f-807a-4d35-aa21-b815435544d0": {
             "model": {
                 "ranges": [],
                 "text": "select m.machine_name as Machine,du.name as DeploymentUnit, t.build_no \r\nfrom `/DPM/DeploymentManager/ToolsOnMachine` as t\r\njoin `/DPM/DeploymentManager/Machine` as m\r\non oid(t.machine_id) = m._id\r\njoin `/DPM/DeploymentManager/DeploymentUnit` as du\r\non oid(t.parent_entity_id)=du._id and du.name=(case when :Entities = \"all\" then du.name else :Entities end) order by du.name asc , m.machine_name asc ,t.build_no desc"
             },
             "cardType": "ace-sql"
         }
     },
        "rootId": "086a06de-49e7-4eb3-a614-a667e77abc47",
        "version": 2
     },
    {
        "collection_name": "Reports.Multiple_Tools_Deployed_On_Machine\.slam.index",
        "decks": {
            "26b8a51d-455a-4e23-a904-83e8836eb16e": {
                "cards": [
                    "e38b6f94-6b20-403d-a033-c0f36ea389ca"
                ],
                "name": ""
            },
            "3261c5f4-a5d8-4954-9b67-fe584d76b13a": {
                "cards": [
                    "f08df053-ff77-4563-9661-0837a801cb0c",
                    "21817249-6008-4852-9f85-7fad74b4afc8",
                    "45198c9c-b861-4e51-babc-db5fbfcd27ce",
                    "6f65a5d9-8973-4534-8749-241567995119"
                ],
                "name": ""
            },
            "35d50c54-09c8-4744-b34b-f9f901547060": {
                "cards": [
                    "f08df053-ff77-4563-9661-0837a801cb0c",
                    "21817249-6008-4852-9f85-7fad74b4afc8"
                ],
                "name": ""
            }
        },
        "cards": {
            "21817249-6008-4852-9f85-7fad74b4afc8": {
                "model": {
                    "state": {
                        "Machine": {
                            "labels": {
                                "value": [
                                      {
                                          "literal": "all"
                                      },
                                    {
                                          "literal": "root123@illin4468"
                                      },
                                    {
                                          "literal": "mpswrk1@10.235.64.253"
                                      },
                                    {
                                          "literal": "mpswrk1@10.235.64.94"
                                      },
                                    {
                                          "literal": "mpswrk1@10.235.66.41"
                                      },
                                    {
                                          "literal": "root@nlate032"
                                      },
                                    {
                                          "literal": "rytr@10.232.262.31"
                                      },
                                    {
                                          "literal": "admin@june20"
                                      },
                                    {
                                          "literal": "Sahil@finaljune20"
                                      },
                                    {
                                          "literal": "test_sahil@test_Sahil"
                                      },
                                    {
                                          "literal": "admin@sahil"
                                      },
                                    {
                                          "literal": "admin@soni"
                                      },
                                    {
                                          "literal": "mpswrk1@10.235.73.14"
                                      },
                                    {
                                          "literal": "10.235.66.41"
                                      },
                                    {
                                          "literal": "root@vptestind01"
                                      },
                                    {
                                          "literal": "abcd@abcd"
                                      }
                                ],
                                "type": "lit"
                            },
                            "selection": {
                                "value": {
                                    "literal": "10.235.66.41"
                                },
                                "type": "lit"
                            },
                            "type": "dropdown"
                        },
                        "beginDate": {
                            "textBox": {
                                "value": {
                                    "value": {
                                        "day": 1,
                                        "month": 1,
                                        "year": 2016
                                    },
                                    "type": "lit"
                                },
                                "type": "date"
                            },
                            "type": "textbox"
                        },
                        "endDate": {
                            "textBox": {
                                "value": {
                                    "value": {
                                        "day": 1,
                                        "month": 1,
                                        "year": 2050
                                    },
                                    "type": "lit"
                                },
                                "type": "date"
                            },
                            "type": "textbox"
                        }
                    },
                    "input": {
                        "blocks": [
                            {
                                "content": [
                                    {
                                        "value": "Select",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "Machine",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "to",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "find",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "all",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "Tools",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "deployed",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "on",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "that",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "machine",
                                        "type": "str"
                                    }
                                ],
                                "level": 2,
                                "type": "header"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "labels": {
                                                "value": [
                                                      {
                                                          "literal": "all"
                                                      },
                                                    {
                                                          "literal": "root123@illin4468"
                                                      },
                                                    {
                                                          "literal": "mpswrk1@10.235.64.253"
                                                      },
                                                    {
                                                          "literal": "mpswrk1@10.235.64.94"
                                                      },
                                                    {
                                                          "literal": "mpswrk1@10.235.66.41"
                                                      },
                                                    {
                                                          "literal": "root@nlate032"
                                                      },
                                                    {
                                                          "literal": "rytr@10.232.262.31"
                                                      },
                                                    {
                                                          "literal": "admin@june20"
                                                      },
                                                    {
                                                          "literal": "Sahil@finaljune20"
                                                      },
                                                    {
                                                          "literal": "test_sahil@test_Sahil"
                                                      },
                                                    {
                                                          "literal": "admin@sahil"
                                                      },
                                                    {
                                                          "literal": "admin@soni"
                                                      },
                                                    {
                                                          "literal": "mpswrk1@10.235.73.14"
                                                      },
                                                    {
                                                          "literal": "10.235.66.41"
                                                      },
                                                    {
                                                          "literal": "root@vptestind01"
                                                      },
                                                    {
                                                          "literal": "abcd@abcd"
                                                      }
                                                ],
                                                "type": "lit"
                                            },
                                            "selection": {
                                                "value": {
                                                    "literal": "all"
                                                },
                                                "type": "lit"
                                            },
                                            "type": "dropdown"
                                        },
                                        "required": False,
                                        "label": "Machine",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "textBox": {
                                                "value": {
                                                    "value": {
                                                        "day": 1,
                                                        "month": 1,
                                                        "year": 2016
                                                    },
                                                    "type": "lit"
                                                },
                                                "type": "date"
                                            },
                                            "type": "textbox"
                                        },
                                        "required": False,
                                        "label": "beginDate",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "textBox": {
                                                "value": {
                                                    "value": {
                                                        "day": 1,
                                                        "month": 1,
                                                        "year": 2050
                                                    },
                                                    "type": "lit"
                                                },
                                                "type": "date"
                                            },
                                            "type": "textbox"
                                        },
                                        "required": False,
                                        "label": "endDate",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            }
                        ],
                        "doc": "slamdown"
                    }
                },
                "cardType": "markdown"
            },
            "45198c9c-b861-4e51-babc-db5fbfcd27ce": {
                "model": {
                    "ranges": [],
                    "text": "--select 10.235.66.41 machine \r\nselect distinct (tool.name) as ToolName,m.machine_name as Machine, t.build_no as Build , v.version_name||\" \"||v.version_number as Version\r\nfrom `/DPM/DeploymentManager/ToolsOnMachine` as t\r\njoin `/DPM/DeploymentManager/Versions` as v\r\non oid(t.parent_entity_id) = v._id\r\njoin `/DPM/DeploymentManager/Tool` as tool\r\non oid(v.tool_id)=tool._id\r\njoin `/DPM/DeploymentManager/Machine` as m\r\non oid(t.machine_id) = m._id and m.machine_name = (case when :Machine = \"all\" then m.machine_name else :Machine end)\r\ngroup by m.machine_name , tool.name , t.build_no order by tool.name asc,t.build_no desc  ,m.machine_name asc"
                },
                "cardType": "ace-sql"
            },
            "6f65a5d9-8973-4534-8749-241567995119": {
                "model": {
                    "pageSize": 25,
                    "page": None
                },
                "cardType": "table"
            },
            "e38b6f94-6b20-403d-a033-c0f36ea389ca": {
                "model": {
                    "layout": {
                        "panes": [
                              {
                                  "pane": {
                                      "panes": [
                                          {
                                              "pane": {
                                                  "value": "35d50c54-09c8-4744-b34b-f9f901547060",
                                                  "type": "cell"
                                              },
                                              "ratio": [
                                                  1,
                                                  1
                                              ]
                                          }
                                      ],
                                      "orientation": "horizontal",
                                      "type": "split"
                                  },
                                  "ratio": [
                                      1,
                                      2
                                  ]
                              },
                            {
                                  "pane": {
                                      "panes": [
                                          {
                                              "pane": {
                                                  "value": "3261c5f4-a5d8-4954-9b67-fe584d76b13a",
                                                  "type": "cell"
                                              },
                                              "ratio": [
                                                  1,
                                                  1
                                              ]
                                          }
                                      ],
                                      "orientation": "horizontal",
                                      "type": "split"
                                  },
                                  "ratio": [
                                      1,
                                      2
                                  ]
                              }
                        ],
                        "orientation": "vertical",
                        "type": "split"
                    }
                },
                "cardType": "draftboard"
            },
            "f08df053-ff77-4563-9661-0837a801cb0c": {
                "model": {
                    "ranges": [],
                    "text": "## Select Machine to find all Tools deployed on that machine\nMachine = {!``select machine_name from `/DPM/DeploymentManager/Machine` ``} (all)\n\nbeginDate = ____-__-__(2016-01-01)\n\nendDate = ____-__-__(2050-01-01)\n"
                },
                "cardType": "ace-markdown"
            }
        },
        "rootId": "26b8a51d-455a-4e23-a904-83e8836eb16e",
        "version": 2
    },
    {"collection_name": "Reports.Successful_Tool_Deployments\.slam.index",
        "decks" : {
        "686abd57-2464-4610-9be6-4ac971779422" : {
            "cards" : [ 
                "ab846277-2504-4736-aa66-5ffcbec0174c", 
                "cdb8b005-bf74-4f2d-bf5e-9ff69d8b0012", 
                "042a23af-49d1-46f1-acae-bd07740c40a9", 
                "a6a54cd6-f563-49d2-8399-e7fd263f4add", 
                "7619d3fd-97c7-46f0-b91c-89a9be9c4ae9", 
                "911ffbb5-23e6-44c3-a3f7-16584236b6d6"
            ],
            "name" : ""
        },
        "6d0d3656-ef3b-4835-82d0-742d7e2e7e9c" : {
            "cards" : [ 
                "ab846277-2504-4736-aa66-5ffcbec0174c", 
                "cdb8b005-bf74-4f2d-bf5e-9ff69d8b0012", 
                "f7d0c686-2f18-4dab-9291-e8f1359f38a5", 
                "36ecb430-7fc5-4d80-bb1d-d8698e3a59d0"
            ],
            "name" : ""
        },
        "b62617b3-150a-4019-a4b8-9bc1ffb104c4" : {
            "cards" : [ 
                "a859ed9c-c3e0-4e45-a565-50beab6fcc04"
            ],
            "name" : ""
        },
        "ec01954a-980e-4d38-b51a-dc29fbd61da2" : {
            "cards" : [ 
                "ab846277-2504-4736-aa66-5ffcbec0174c", 
                "cdb8b005-bf74-4f2d-bf5e-9ff69d8b0012"
            ],
            "name" : ""
        }
    },
    "cards" : {
        "042a23af-49d1-46f1-acae-bd07740c40a9" : {
            "model" : {
                "ranges" : [],
                "text" : "select count(dr._id) as count ,dr.status , t.name  from `/DPM/DeploymentManager/DeploymentRequest`as dr \r\njoin `/DPM/DeploymentManager/Versions`as v on oid(dr.parent_entity_id) =v._id join `/DPM/DeploymentManager/Tool` as t on \r\nt._id = oid(v.tool_id ) and  dr.deployment_type = \"toolgroup\" and t.name = ( case when :Entities = \"all\" then t.name else :Entities end ) group by t.name,dr.status"
            },
            "cardType" : "ace-sql"
        },
        "36ecb430-7fc5-4d80-bb1d-d8698e3a59d0" : {
            "model" : {
                "state" : {},
                "input" : {
                    "blocks" : [],
                    "doc" : "slamdown"
                }
            },
            "cardType" : "markdown"
        },
        "7619d3fd-97c7-46f0-b91c-89a9be9c4ae9" : {
            "model" : {
                "axisLabelAngle" : 0,
                "parallel" : None,
                "stack" : [ 
                    "status"
                ],
                "valueAggregation" : "Sum",
                "value" : [ 
                    "count"
                ],
                "category" : [ 
                    "name"
                ],
                "configType" : "bar"
            },
            "cardType" : "bar-options"
        },
        "911ffbb5-23e6-44c3-a3f7-16584236b6d6" : {
            "model" : None,
            "cardType" : "chart"
        },
        "a6a54cd6-f563-49d2-8399-e7fd263f4add" : {
            "model" : {
                "pageSize" : None,
                "page" : None
            },
            "cardType" : "table"
        },
        "a859ed9c-c3e0-4e45-a565-50beab6fcc04" : {
            "model" : {
                "layout" : {
                    "panes" : [ 
                        {
                            "pane" : {
                                "panes" : [ 
                                    {
                                        "pane" : {
                                            "panes" : [ 
                                                {
                                                    "pane" : {
                                                        "value" : "ec01954a-980e-4d38-b51a-dc29fbd61da2",
                                                        "type" : "cell"
                                                    },
                                                    "ratio" : [ 
                                                        1, 
                                                        1
                                                    ]
                                                }
                                            ],
                                            "orientation" : "vertical",
                                            "type" : "split"
                                        },
                                        "ratio" : [ 
                                            1, 
                                            2
                                        ]
                                    }, 
                                    {
                                        "pane" : {
                                            "panes" : [ 
                                                {
                                                    "pane" : {
                                                        "value" : "6d0d3656-ef3b-4835-82d0-742d7e2e7e9c",
                                                        "type" : "cell"
                                                    },
                                                    "ratio" : [ 
                                                        1, 
                                                        1
                                                    ]
                                                }
                                            ],
                                            "orientation" : "vertical",
                                            "type" : "split"
                                        },
                                        "ratio" : [ 
                                            1, 
                                            2
                                        ]
                                    }
                                ],
                                "orientation" : "horizontal",
                                "type" : "split"
                            },
                            "ratio" : [ 
                                1, 
                                2
                            ]
                        }, 
                        {
                            "pane" : {
                                "panes" : [ 
                                    {
                                        "pane" : {
                                            "value" : "686abd57-2464-4610-9be6-4ac971779422",
                                            "type" : "cell"
                                        },
                                        "ratio" : [ 
                                            1, 
                                            1
                                        ]
                                    }
                                ],
                                "orientation" : "horizontal",
                                "type" : "split"
                            },
                            "ratio" : [ 
                                1, 
                                2
                            ]
                        }
                    ],
                    "orientation" : "vertical",
                    "type" : "split"
                }
            },
            "cardType" : "draftboard"
        },
        "ab846277-2504-4736-aa66-5ffcbec0174c" : {
            "model" : {
                "ranges" : [],
                "text" : "# Report to find Percentage of Sucessfull Deployments of Tool  \r\n\r\n## Please select the Tool \r\n\r\nEntities = {!``  Select name from `/DPM/DeploymentManager/Tool` order by name ``} (all)"
            },
            "cardType" : "ace-markdown"
        },
        "cdb8b005-bf74-4f2d-bf5e-9ff69d8b0012" : {
            "model" : {
                "state" : {
                    "Entities" : {
                        "labels" : {
                            "value" : [ 
                                {
                                    "literal" : "all"
                                }, 
                                {
                                    "literal" : "AC Rebuild Map"
                                }, 
                                {
                                    "literal" : "ATOOLISSUE"
                                }, 
                                {
                                    "literal" : "Amdocs Data Loader"
                                }, 
                                {
                                    "literal" : "Ansible"
                                }, 
                                {
                                    "literal" : "Argus"
                                }, 
                                {
                                    "literal" : "BAP Error Report"
                                }, 
                                {
                                    "literal" : "BAP Failed Transaction Processing"
                                }, 
                                {
                                    "literal" : "BCC Health Check Report"
                                }, 
                                {
                                    "literal" : "BI Dashboard ETL"
                                }, 
                                {
                                    "literal" : "BI Dashboard UI"
                                }, 
                                {
                                    "literal" : "Beats"
                                }, 
                                {
                                    "literal" : "Bill Cycle Summary Report"
                                }, 
                                {
                                    "literal" : "Cancel Old Pending Orders"
                                }, 
                                {
                                    "literal" : "Collection Queue Report"
                                }, 
                                {
                                    "literal" : "Collection Request Automation"
                                }, 
                                {
                                    "literal" : "Collection Roundtrip"
                                }, 
                                {
                                    "literal" : "Collection Status Kpi"
                                }, 
                                {
                                    "literal" : "CopyBAN Self Service"
                                }, 
                                {
                                    "literal" : "DB Compare Script"
                                }, 
                                {
                                    "literal" : "DB HF Verification"
                                }, 
                                {
                                    "literal" : "DB Incremental Apply"
                                }, 
                                {
                                    "literal" : "DB Session Check"
                                }, 
                                {
                                    "literal" : "Deployment Manager"
                                }, 
                                {
                                    "literal" : "Direct Debit Recon"
                                }, 
                                {
                                    "literal" : "Distributed Environment Installation"
                                }, 
                                {
                                    "literal" : "Elasticsearch"
                                }, 
                                {
                                    "literal" : "GSS EAAS BE"
                                }, 
                                {
                                    "literal" : "Gin1"
                                }, 
                                {
                                    "literal" : "Ginger"
                                }, 
                                {
                                    "literal" : "Ginna"
                                }, 
                                {
                                    "literal" : "Gitech Self Service"
                                }, 
                                {
                                    "literal" : "HP Diagnostic Server"
                                }, 
                                {
                                    "literal" : "HP Diagnostics Probe"
                                }, 
                                {
                                    "literal" : "Interaction Case Count Report"
                                }, 
                                {
                                    "literal" : "Junk Character Validation"
                                }, 
                                {
                                    "literal" : "KetkiNewTool"
                                }, 
                                {
                                    "literal" : "Kibana"
                                }, 
                                {
                                    "literal" : "Krrish"
                                }, 
                                {
                                    "literal" : "Log Pattern Search Report"
                                }, 
                                {
                                    "literal" : "Logstash"
                                }, 
                                {
                                    "literal" : "Long Running Queries"
                                }, 
                                {
                                    "literal" : "MCO"
                                }, 
                                {
                                    "literal" : "MCO Templates"
                                }, 
                                {
                                    "literal" : "MFS DB Archive"
                                }, 
                                {
                                    "literal" : "Minions"
                                }, 
                                {
                                    "literal" : "NGM OM Agent"
                                }, 
                                {
                                    "literal" : "OMS Data Issue Analysis"
                                }, 
                                {
                                    "literal" : "One Click Billing"
                                }, 
                                {
                                    "literal" : "Oracle Empty Database Creation"
                                }, 
                                {
                                    "literal" : "Order Action Status"
                                }, 
                                {
                                    "literal" : "Prepaid TC Monitoring"
                                }, 
                                {
                                    "literal" : "Probe Order"
                                }, 
                                {
                                    "literal" : "Production Reports"
                                }, 
                                {
                                    "literal" : "Rated Events and PI Mismatch Report"
                                }, 
                                {
                                    "literal" : "Real Time Monitoring"
                                }, 
                                {
                                    "literal" : "Reconciliation"
                                }, 
                                {
                                    "literal" : "Refund Recon"
                                }, 
                                {
                                    "literal" : "SASS"
                                }, 
                                {
                                    "literal" : "SSS"
                                }, 
                                {
                                    "literal" : "Satellite Templates"
                                }, 
                                {
                                    "literal" : "SpyStudio"
                                }, 
                                {
                                    "literal" : "Stuck Order Aging Report"
                                }, 
                                {
                                    "literal" : "Stuck Order Error Report"
                                }, 
                                {
                                    "literal" : "Stuck Order Report"
                                }, 
                                {
                                    "literal" : "TC Monitoring Throughput Error Report"
                                }, 
                                {
                                    "literal" : "TOOL1"
                                }, 
                                {
                                    "literal" : "TOOLER"
                                }, 
                                {
                                    "literal" : "TRB Error Report"
                                }, 
                                {
                                    "literal" : "TRB Main Map"
                                }, 
                                {
                                    "literal" : "TRB Recycle"
                                }, 
                                {
                                    "literal" : "Telegraf Agent"
                                }, 
                                {
                                    "literal" : "Test"
                                }, 
                                {
                                    "literal" : "Test Depricate"
                                }, 
                                {
                                    "literal" : "Test0YF1S7"
                                }, 
                                {
                                    "literal" : "Test833"
                                }, 
                                {
                                    "literal" : "TestSahil"
                                }, 
                                {
                                    "literal" : "Unified Operations Console"
                                }, 
                                {
                                    "literal" : "Usage Freshness"
                                }, 
                                {
                                    "literal" : "Usage Hourly Processing Statistic"
                                }, 
                                {
                                    "literal" : "Usage Recon Daily Extract"
                                }, 
                                {
                                    "literal" : "Usage Success Rates"
                                }, 
                                {
                                    "literal" : "Usage throughput and error"
                                }, 
                                {
                                    "literal" : "XPack"
                                }, 
                                {
                                    "literal" : "bdbd"
                                }, 
                                {
                                    "literal" : "c"
                                }, 
                                {
                                    "literal" : "demooleg"
                                }, 
                                {
                                    "literal" : "jTrace"
                                }, 
                                {
                                    "literal" : "name"
                                }, 
                                {
                                    "literal" : "newTool"
                                }, 
                                {
                                    "literal" : "nmnbm"
                                }, 
                                {
                                    "literal" : "ok"
                                }, 
                                {
                                    "literal" : "pdTOOL"
                                }, 
                                {
                                    "literal" : "qwerty"
                                }, 
                                {
                                    "literal" : "shyamji regression"
                                }, 
                                {
                                    "literal" : "shyamjitool"
                                }, 
                                {
                                    "literal" : "test tool  300"
                                }, 
                                {
                                    "literal" : "test1"
                                }, 
                                {
                                    "literal" : "testing"
                                }, 
                                {
                                    "literal" : "testshyam"
                                }, 
                                {
                                    "literal" : "vfnn"
                                }
                            ],
                            "type" : "lit"
                        },
                        "selection" : {
                            "value" : {
                                "literal" : "Usage Hourly Processing Statistic"
                            },
                            "type" : "lit"
                        },
                        "type" : "dropdown"
                    }
                },
                "input" : {
                    "blocks" : [ 
                        {
                            "content" : [ 
                                {
                                    "value" : "Report",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "to",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "find",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "Percentage",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "of",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "Sucessfull",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "Deployments",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "of",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "Tool",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }
                            ],
                            "level" : 1,
                            "type" : "header"
                        }, 
                        {
                            "content" : [ 
                                {
                                    "type" : "space"
                                }
                            ],
                            "type" : "para"
                        }, 
                        {
                            "content" : [ 
                                {
                                    "value" : "Please",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "select",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "the",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "Tool",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }
                            ],
                            "level" : 2,
                            "type" : "header"
                        }, 
                        {
                            "content" : [ 
                                {
                                    "type" : "softbreak"
                                }, 
                                {
                                    "field" : {
                                        "labels" : {
                                            "value" : [ 
                                                {
                                                    "literal" : "all"
                                                }, 
                                                {
                                                    "literal" : "AC Rebuild Map"
                                                }, 
                                                {
                                                    "literal" : "ATOOLISSUE"
                                                }, 
                                                {
                                                    "literal" : "Amdocs Data Loader"
                                                }, 
                                                {
                                                    "literal" : "Ansible"
                                                }, 
                                                {
                                                    "literal" : "Argus"
                                                }, 
                                                {
                                                    "literal" : "BAP Error Report"
                                                }, 
                                                {
                                                    "literal" : "BAP Failed Transaction Processing"
                                                }, 
                                                {
                                                    "literal" : "BCC Health Check Report"
                                                }, 
                                                {
                                                    "literal" : "BI Dashboard ETL"
                                                }, 
                                                {
                                                    "literal" : "BI Dashboard UI"
                                                }, 
                                                {
                                                    "literal" : "Beats"
                                                }, 
                                                {
                                                    "literal" : "Bill Cycle Summary Report"
                                                }, 
                                                {
                                                    "literal" : "Cancel Old Pending Orders"
                                                }, 
                                                {
                                                    "literal" : "Collection Queue Report"
                                                }, 
                                                {
                                                    "literal" : "Collection Request Automation"
                                                }, 
                                                {
                                                    "literal" : "Collection Roundtrip"
                                                }, 
                                                {
                                                    "literal" : "Collection Status Kpi"
                                                }, 
                                                {
                                                    "literal" : "CopyBAN Self Service"
                                                }, 
                                                {
                                                    "literal" : "DB Compare Script"
                                                }, 
                                                {
                                                    "literal" : "DB HF Verification"
                                                }, 
                                                {
                                                    "literal" : "DB Incremental Apply"
                                                }, 
                                                {
                                                    "literal" : "DB Session Check"
                                                }, 
                                                {
                                                    "literal" : "Deployment Manager"
                                                }, 
                                                {
                                                    "literal" : "Direct Debit Recon"
                                                }, 
                                                {
                                                    "literal" : "Distributed Environment Installation"
                                                }, 
                                                {
                                                    "literal" : "Elasticsearch"
                                                }, 
                                                {
                                                    "literal" : "GSS EAAS BE"
                                                }, 
                                                {
                                                    "literal" : "Gin1"
                                                }, 
                                                {
                                                    "literal" : "Ginger"
                                                }, 
                                                {
                                                    "literal" : "Ginna"
                                                }, 
                                                {
                                                    "literal" : "Gitech Self Service"
                                                }, 
                                                {
                                                    "literal" : "HP Diagnostic Server"
                                                }, 
                                                {
                                                    "literal" : "HP Diagnostics Probe"
                                                }, 
                                                {
                                                    "literal" : "Interaction Case Count Report"
                                                }, 
                                                {
                                                    "literal" : "Junk Character Validation"
                                                }, 
                                                {
                                                    "literal" : "KetkiNewTool"
                                                }, 
                                                {
                                                    "literal" : "Kibana"
                                                }, 
                                                {
                                                    "literal" : "Krrish"
                                                }, 
                                                {
                                                    "literal" : "Log Pattern Search Report"
                                                }, 
                                                {
                                                    "literal" : "Logstash"
                                                }, 
                                                {
                                                    "literal" : "Long Running Queries"
                                                }, 
                                                {
                                                    "literal" : "MCO"
                                                }, 
                                                {
                                                    "literal" : "MCO Templates"
                                                }, 
                                                {
                                                    "literal" : "MFS DB Archive"
                                                }, 
                                                {
                                                    "literal" : "Minions"
                                                }, 
                                                {
                                                    "literal" : "NGM OM Agent"
                                                }, 
                                                {
                                                    "literal" : "OMS Data Issue Analysis"
                                                }, 
                                                {
                                                    "literal" : "One Click Billing"
                                                }, 
                                                {
                                                    "literal" : "Oracle Empty Database Creation"
                                                }, 
                                                {
                                                    "literal" : "Order Action Status"
                                                }, 
                                                {
                                                    "literal" : "Prepaid TC Monitoring"
                                                }, 
                                                {
                                                    "literal" : "Probe Order"
                                                }, 
                                                {
                                                    "literal" : "Production Reports"
                                                }, 
                                                {
                                                    "literal" : "Rated Events and PI Mismatch Report"
                                                }, 
                                                {
                                                    "literal" : "Real Time Monitoring"
                                                }, 
                                                {
                                                    "literal" : "Reconciliation"
                                                }, 
                                                {
                                                    "literal" : "Refund Recon"
                                                }, 
                                                {
                                                    "literal" : "SASS"
                                                }, 
                                                {
                                                    "literal" : "SSS"
                                                }, 
                                                {
                                                    "literal" : "Satellite Templates"
                                                }, 
                                                {
                                                    "literal" : "SpyStudio"
                                                }, 
                                                {
                                                    "literal" : "Stuck Order Aging Report"
                                                }, 
                                                {
                                                    "literal" : "Stuck Order Error Report"
                                                }, 
                                                {
                                                    "literal" : "Stuck Order Report"
                                                }, 
                                                {
                                                    "literal" : "TC Monitoring Throughput Error Report"
                                                }, 
                                                {
                                                    "literal" : "TOOL1"
                                                }, 
                                                {
                                                    "literal" : "TOOLER"
                                                }, 
                                                {
                                                    "literal" : "TRB Error Report"
                                                }, 
                                                {
                                                    "literal" : "TRB Main Map"
                                                }, 
                                                {
                                                    "literal" : "TRB Recycle"
                                                }, 
                                                {
                                                    "literal" : "Telegraf Agent"
                                                }, 
                                                {
                                                    "literal" : "Test"
                                                }, 
                                                {
                                                    "literal" : "Test Depricate"
                                                }, 
                                                {
                                                    "literal" : "Test0YF1S7"
                                                }, 
                                                {
                                                    "literal" : "Test833"
                                                }, 
                                                {
                                                    "literal" : "TestSahil"
                                                }, 
                                                {
                                                    "literal" : "Unified Operations Console"
                                                }, 
                                                {
                                                    "literal" : "Usage Freshness"
                                                }, 
                                                {
                                                    "literal" : "Usage Hourly Processing Statistic"
                                                }, 
                                                {
                                                    "literal" : "Usage Recon Daily Extract"
                                                }, 
                                                {
                                                    "literal" : "Usage Success Rates"
                                                }, 
                                                {
                                                    "literal" : "Usage throughput and error"
                                                }, 
                                                {
                                                    "literal" : "XPack"
                                                }, 
                                                {
                                                    "literal" : "bdbd"
                                                }, 
                                                {
                                                    "literal" : "c"
                                                }, 
                                                {
                                                    "literal" : "demooleg"
                                                }, 
                                                {
                                                    "literal" : "jTrace"
                                                }, 
                                                {
                                                    "literal" : "name"
                                                }, 
                                                {
                                                    "literal" : "newTool"
                                                }, 
                                                {
                                                    "literal" : "nmnbm"
                                                }, 
                                                {
                                                    "literal" : "ok"
                                                }, 
                                                {
                                                    "literal" : "pdTOOL"
                                                }, 
                                                {
                                                    "literal" : "qwerty"
                                                }, 
                                                {
                                                    "literal" : "shyamji regression"
                                                }, 
                                                {
                                                    "literal" : "shyamjitool"
                                                }, 
                                                {
                                                    "literal" : "test tool  300"
                                                }, 
                                                {
                                                    "literal" : "test1"
                                                }, 
                                                {
                                                    "literal" : "testing"
                                                }, 
                                                {
                                                    "literal" : "testshyam"
                                                }, 
                                                {
                                                    "literal" : "vfnn"
                                                }
                                            ],
                                            "type" : "lit"
                                        },
                                        "selection" : {
                                            "value" : {
                                                "literal" : "all"
                                            },
                                            "type" : "lit"
                                        },
                                        "type" : "dropdown"
                                    },
                                    "required" : False,
                                    "label" : "Entities",
                                    "type" : "field"
                                }
                            ],
                            "type" : "para"
                        }
                    ],
                    "doc" : "slamdown"
                }
            },
            "cardType" : "markdown"
        },
        "f7d0c686-2f18-4dab-9291-e8f1359f38a5" : {
            "model" : {
                "ranges" : [],
                "text" : "# Statistics for Deployments :\r\n\r\n1. There were total !``select count(d._id) as count , d.status  from `/DPM/DeploymentManager/DeploymentRequest` as d join `/DPM/DeploymentManager/Versions` as v on oid(d.parent_entity_id )= v._id \r\n   join `/DPM/DeploymentManager/Tool` as t on oid(v.tool_id) = t._id and t.name = ( case when :Entities = \"all\" then t.name else :Entities end ) group by d.status \r\n   `` Deployment requests submitted for !``:Entities`` tool.\r\n    \r\n2. !``:Entities`` Tool was deployed on !``select count(distinct d.machine_id) from `/DPM/DeploymentManager/DeploymentRequest` as d join `/DPM/DeploymentManager/Versions` as v on oid(d.parent_entity_id) = v._id\r\n   join `/DPM/DeploymentManager/Tool` as t on oid(v.tool_id) = t._id and t.name = ( case when :Entities = \"all\" then t.name else :Entities end ) group by t.name`` machines .\r\n    \r\n3. Total Sucessfull Deployment Requests : !``select count(d._id) from `/DPM/DeploymentManager/DeploymentRequest` as d join `/DPM/DeploymentManager/Versions` as v on (oid(d.parent_entity_id) = v._id \r\n   and d.status = \"Done\" ) join `/DPM/DeploymentManager/Tool` as t on oid(v.tool_id) = t._id and t.name = ( case when :Entities = \"all\" then t.name else :Entities end )``\r\n   \r\n4. Total failed Deployment Requests : !``select count(d._id)  from `/DPM/DeploymentManager/DeploymentRequest` as d join `/DPM/DeploymentManager/Versions` as v on (oid(d.parent_entity_id) = v._id \r\n   and d.status = \"Failed\" ) join `/DPM/DeploymentManager/Tool` as t on oid(v.tool_id) = t._id and t.name = ( case when :Entities = \"all\" then t.name else :Entities end )``\r\n\r\n# Average time for Deployments of Tool :\r\n\r\n1. The Average RUN_TIME for Successfull deployments for tool !``:Entities`` are = !``select t.name ,AVG((d.end_time-d.start_time) / 60000) as Average_time from `/DPM/DeploymentManager/DeploymentRequest` as d \r\n   join `/DPM/DeploymentManager/Versions`as v on oid(d.parent_entity_id) = v._id join `/DPM/DeploymentManager/Tool` as t on t._id = oid(v.tool_id ) and d.status=\"Done\" and t.name = ( case when :Entities = \"all\" then t.name else :Entities end )group by t.name ``\r\n   \r\n2. Average for recent failed deployments to first consecutive sucessfull deployment for tool !``:Entities`` are =!``select AVG((f.end_time-x.end_time)/60000) as diffrence_time from (select t.name,d.end_time from `/DPM/DeploymentManager/DeploymentRequest` as d join \r\n   `/DPM/DeploymentManager/Versions`as v on oid(d.parent_entity_id) = v._id join `/DPM/DeploymentManager/Tool` as t on t._id = oid(v.tool_id ) and d.status = \"Failed\" and t.name = ( case when :Entities = \"all\" then t.name else :Entities end ) group by t.name) as x \r\n   inner join (select   t1.name,d1.end_time from `/DPM/DeploymentManager/DeploymentRequest` as d1 join `/DPM/DeploymentManager/Versions`as v1 \r\n   on oid(d1.parent_entity_id) = v1._id join `/DPM/DeploymentManager/Tool` as t1 on t1._id = oid(v1.tool_id ) where d1.status = \"Done\" and t1.name = ( case when :Entities = \"all\" then t1.name else :Entities end )\r\n   group by t1.name) as f on f.name = x.name ``  \r\n"
            },
            "cardType" : "ace-markdown"
        }
    },
    "rootId" : "b62617b3-150a-4019-a4b8-9bc1ffb104c4",
    "version" : 2
     },

    {
        "collection_name": "Reports.Successful_DU_Deployments\.slam.index",
        "decks" : {
        "686abd57-2464-4610-9be6-4ac971779422" : {
            "cards" : [ 
                "ab846277-2504-4736-aa66-5ffcbec0174c", 
                "cdb8b005-bf74-4f2d-bf5e-9ff69d8b0012", 
                "74f78b52-b04f-471f-975e-bdb926e0ea02", 
                "00398c31-2f6f-486f-b0fc-1a66ee7a6295", 
                "52718842-af7a-482d-a288-e129c8208505", 
                "360c4e9b-4592-43f5-a9d8-7cc21bc2acb7"
            ],
            "name" : ""
        },
        "b62617b3-150a-4019-a4b8-9bc1ffb104c4" : {
            "cards" : [ 
                "a859ed9c-c3e0-4e45-a565-50beab6fcc04"
            ],
            "name" : ""
        },
        "bbf3f576-08b6-4cc1-b988-5a14b34446ac" : {
            "cards" : [ 
                "ab846277-2504-4736-aa66-5ffcbec0174c", 
                "cdb8b005-bf74-4f2d-bf5e-9ff69d8b0012", 
                "dc18bd06-ccb6-4674-b427-350cfbd248b5", 
                "6a9a99c9-a8e0-4f50-89f8-1fa7bf4195ad"
            ],
            "name" : ""
        },
        "ec01954a-980e-4d38-b51a-dc29fbd61da2" : {
            "cards" : [ 
                "ab846277-2504-4736-aa66-5ffcbec0174c", 
                "cdb8b005-bf74-4f2d-bf5e-9ff69d8b0012"
            ],
            "name" : ""
        }
    },
    "cards" : {
        "00398c31-2f6f-486f-b0fc-1a66ee7a6295" : {
            "model" : {
                "pageSize" : None,
                "page" : None
            },
            "cardType" : "table"
        },
        "360c4e9b-4592-43f5-a9d8-7cc21bc2acb7" : {
            "model" : None,
            "cardType" : "chart"
        },
        "52718842-af7a-482d-a288-e129c8208505" : {
            "model" : {
                "axisLabelAngle" : 0,
                "parallel" : None,
                "stack" : [ 
                    "status"
                ],
                "valueAggregation" : "Sum",
                "value" : [ 
                    "total"
                ],
                "category" : [ 
                    "name"
                ],
                "configType" : "bar"
            },
            "cardType" : "bar-options"
        },
        "6a9a99c9-a8e0-4f50-89f8-1fa7bf4195ad" : {
            "model" : {
                "state" : {},
                "input" : {
                    "blocks" : [],
                    "doc" : "slamdown"
                }
            },
            "cardType" : "markdown"
        },
        "74f78b52-b04f-471f-975e-bdb926e0ea02" : {
            "model" : {
                "ranges" : [],
                "text" : "select count(dr._id) as total, dr.status , du.name\r\nfrom `/DPM/DeploymentManager/DeploymentUnit` as du \r\njoin `/DPM/DeploymentManager/DeploymentRequest`as dr\r\non oid(dr.parent_entity_id) =du._id and dr.deployment_type = \"dugroup\" \r\nand du.name = ( case when :Entities = \"all\" then du.name else :Entities end ) group by du.name,dr.status"
            },
            "cardType" : "ace-sql"
        },
        "a859ed9c-c3e0-4e45-a565-50beab6fcc04" : {
            "model" : {
                "layout" : {
                    "panes" : [ 
                        {
                            "pane" : {
                                "panes" : [ 
                                    {
                                        "pane" : {
                                            "panes" : [ 
                                                {
                                                    "pane" : {
                                                        "value" : "ec01954a-980e-4d38-b51a-dc29fbd61da2",
                                                        "type" : "cell"
                                                    },
                                                    "ratio" : [ 
                                                        1, 
                                                        1
                                                    ]
                                                }
                                            ],
                                            "orientation" : "vertical",
                                            "type" : "split"
                                        },
                                        "ratio" : [ 
                                            1, 
                                            2
                                        ]
                                    }, 
                                    {
                                        "pane" : {
                                            "panes" : [ 
                                                {
                                                    "pane" : {
                                                        "value" : "bbf3f576-08b6-4cc1-b988-5a14b34446ac",
                                                        "type" : "cell"
                                                    },
                                                    "ratio" : [ 
                                                        1, 
                                                        1
                                                    ]
                                                }
                                            ],
                                            "orientation" : "vertical",
                                            "type" : "split"
                                        },
                                        "ratio" : [ 
                                            1, 
                                            2
                                        ]
                                    }
                                ],
                                "orientation" : "horizontal",
                                "type" : "split"
                            },
                            "ratio" : [ 
                                1, 
                                2
                            ]
                        }, 
                        {
                            "pane" : {
                                "panes" : [ 
                                    {
                                        "pane" : {
                                            "value" : "686abd57-2464-4610-9be6-4ac971779422",
                                            "type" : "cell"
                                        },
                                        "ratio" : [ 
                                            1, 
                                            1
                                        ]
                                    }
                                ],
                                "orientation" : "horizontal",
                                "type" : "split"
                            },
                            "ratio" : [ 
                                1, 
                                2
                            ]
                        }
                    ],
                    "orientation" : "vertical",
                    "type" : "split"
                }
            },
            "cardType" : "draftboard"
        },
        "ab846277-2504-4736-aa66-5ffcbec0174c" : {
            "model" : {
                "ranges" : [],
                "text" : "# Report to determine DeploymentUnit Success % of Deployments:\n\n### Please select a DeploymentUnit :\n\nEntities = {!`` Select name from `/DPM/DeploymentManager/DeploymentUnit` order by name ``} (all)\n\n\nbeginDate = ____-__-__(2016-01-01)\n\n\nendDate = ____-__-__(2050-01-01)"
            },
            "cardType" : "ace-markdown"
        },
        "cdb8b005-bf74-4f2d-bf5e-9ff69d8b0012" : {
            "model" : {
                "state" : {
                    "Entities" : {
                        "labels" : {
                            "value" : [ 
                                {
                                    "literal" : "all"
                                }, 
                                {
                                    "literal" : "POCCrmClient9V3800"
                                }, 
                                {
                                    "literal" : "Test DU 2"
                                }, 
                                {
                                    "literal" : "Test DU1"
                                }, 
                                {
                                    "literal" : "Test_stuti"
                                }, 
                                {
                                    "literal" : "gg"
                                }, 
                                {
                                    "literal" : "test 111"
                                }, 
                                {
                                    "literal" : "uyk"
                                }
                            ],
                            "type" : "lit"
                        },
                        "selection" : {
                            "value" : {
                                "literal" : "Test DU 2"
                            },
                            "type" : "lit"
                        },
                        "type" : "dropdown"
                    },
                    "beginDate" : {
                        "textBox" : {
                            "value" : {
                                "value" : {
                                    "day" : 1,
                                    "month" : 1,
                                    "year" : 2016
                                },
                                "type" : "lit"
                            },
                            "type" : "date"
                        },
                        "type" : "textbox"
                    },
                    "endDate" : {
                        "textBox" : {
                            "value" : {
                                "value" : {
                                    "day" : 1,
                                    "month" : 1,
                                    "year" : 2050
                                },
                                "type" : "lit"
                            },
                            "type" : "date"
                        },
                        "type" : "textbox"
                    }
                },
                "input" : {
                    "blocks" : [ 
                        {
                            "content" : [ 
                                {
                                    "value" : "Report",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "to",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "determine",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "DeploymentUnit",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "Success",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "%",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "of",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "Deployments:",
                                    "type" : "str"
                                }
                            ],
                            "level" : 1,
                            "type" : "header"
                        }, 
                        {
                            "content" : [ 
                                {
                                    "value" : "Please",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "select",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "a",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "DeploymentUnit",
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : ":",
                                    "type" : "str"
                                }
                            ],
                            "level" : 3,
                            "type" : "header"
                        }, 
                        {
                            "content" : [ 
                                {
                                    "field" : {
                                        "labels" : {
                                            "value" : [ 
                                                {
                                                    "literal" : "all"
                                                }, 
                                                {
                                                    "literal" : "POCCrmClient9V3800"
                                                }, 
                                                {
                                                    "literal" : "Test DU 2"
                                                }, 
                                                {
                                                    "literal" : "Test DU1"
                                                }, 
                                                {
                                                    "literal" : "Test_stuti"
                                                }, 
                                                {
                                                    "literal" : "gg"
                                                }, 
                                                {
                                                    "literal" : "test 111"
                                                }, 
                                                {
                                                    "literal" : "uyk"
                                                }
                                            ],
                                            "type" : "lit"
                                        },
                                        "selection" : {
                                            "value" : {
                                                "literal" : "all"
                                            },
                                            "type" : "lit"
                                        },
                                        "type" : "dropdown"
                                    },
                                    "required" : False,
                                    "label" : "Entities",
                                    "type" : "field"
                                }
                            ],
                            "type" : "para"
                        }, 
                        {
                            "content" : [ 
                                {
                                    "field" : {
                                        "textBox" : {
                                            "value" : {
                                                "value" : {
                                                    "day" : 1,
                                                    "month" : 1,
                                                    "year" : 2016
                                                },
                                                "type" : "lit"
                                            },
                                            "type" : "date"
                                        },
                                        "type" : "textbox"
                                    },
                                    "required" : False,
                                    "label" : "beginDate",
                                    "type" : "field"
                                }
                            ],
                            "type" : "para"
                        }, 
                        {
                            "content" : [ 
                                {
                                    "field" : {
                                        "textBox" : {
                                            "value" : {
                                                "value" : {
                                                    "day" : 1,
                                                    "month" : 1,
                                                    "year" : 2050
                                                },
                                                "type" : "lit"
                                            },
                                            "type" : "date"
                                        },
                                        "type" : "textbox"
                                    },
                                    "required" : False,
                                    "label" : "endDate",
                                    "type" : "field"
                                }
                            ],
                            "type" : "para"
                        }
                    ],
                    "doc" : "slamdown"
                }
            },
            "cardType" : "markdown"
        },
        "dc18bd06-ccb6-4674-b427-350cfbd248b5" : {
            "model" : {
                "ranges" : [],
                "text" : "# Statistics for Deployments :\r\n\r\n1. There were total !``select count(dr._id) , dr.status from `/DPM/DeploymentManager/DeploymentUnit` as du join `/DPM/DeploymentManager/DeploymentRequest`as dr on oid(dr.parent_entity_id) =du._id and dr.deployment_type = \"dugroup\" \r\n    and du.name = ( case when :Entities = \"all\" then du.name else :Entities end ) group by dr.status`` Deployment requests submitted for !``:Entities`` DeploymentUnit.\r\n    \r\n2. !``:Entities`` DeploymentUnit was deployed on !``select count(distinct dr.machine_id) from `/DPM/DeploymentManager/DeploymentUnit` as du join `/DPM/DeploymentManager/DeploymentRequest`as dr on oid(dr.parent_entity_id) =du._id and dr.deployment_type = \"dugroup\" \r\n    and du.name = ( case when :Entities = \"all\" then du.name else :Entities end ) group by du.name`` machines.\r\n    \r\n3. Total Sucessfull Deployment Requests : !``select count(dr._id) from `/DPM/DeploymentManager/DeploymentUnit` as du join `/DPM/DeploymentManager/DeploymentRequest`as dr on oid(dr.parent_entity_id) =du._id and dr.deployment_type = \"dugroup\" \r\n    and  dr.status = \"Done\" and du.name = ( case when :Entities = \"all\" then du.name else :Entities end )``\r\n    \r\n4. Total failed Deployment Requests : !``select count(dr._id) from `/DPM/DeploymentManager/DeploymentUnit` as du join `/DPM/DeploymentManager/DeploymentRequest`as dr on oid(dr.parent_entity_id) =du._id and dr.deployment_type = \"dugroup\" \r\n    and  dr.status = \"Failed\" and du.name = ( case when :Entities = \"all\" then du.name else :Entities end )``\r\n\r\n\r\n# Average time for Deployments of DU :\r\n\r\n1. The Average RUN_TIME for Successfull deployments for DeploymentUnit !``:Entities`` are = !``select du.name ,AVG((d.end_time-d.start_time) / 60000) as Average_time from `/DPM/DeploymentManager/DeploymentRequest` as d \r\n   join `/DPM/DeploymentManager/DeploymentUnit`as du on oid(d.parent_entity_id) = du._id and d.deployment_type = \"dugroup\" and d.status=\"Done\" and du.name = ( case when :Entities = \"all\" then du.name else :Entities end )group by du.name ``\r\n   \r\n2. Average for recent failed deployments to first consecutive sucessfull deployment for DeploymentUnit !``:Entities`` are =!``select AVG((f.end_time-x.end_time)/60000) as diffrence_time from (select du.name,d.end_time from `/DPM/DeploymentManager/DeploymentRequest` as d \r\n   join `/DPM/DeploymentManager/DeploymentUnit`as du on oid(d.parent_entity_id) = du._id and d.status = \"Failed\" and d.deployment_type = \"dugroup\" and du.name = ( case when :Entities = \"all\" then du.name else :Entities end ) group by du.name) as x \r\n   inner join (select   du1.name,d1.end_time from `/DPM/DeploymentManager/DeploymentRequest` as d1 join `/DPM/DeploymentManager/DeploymentUnit`as du1 \r\n   on oid(d1.parent_entity_id) = du1._id where d1.status = \"Done\" and  d1.deployment_type = \"dugroup\" and du1.name = ( case when :Entities = \"all\" then du1.name else :Entities end )\r\n   group by du1.name) as f on f.name = x.name ``\r\n"
            },
            "cardType" : "ace-markdown"
        }
    },
    "rootId" : "b62617b3-150a-4019-a4b8-9bc1ffb104c4",
    "version" : 2
    },
    {
        "collection_name": "Reports.Tool_Deployed_On_Multiple_Machines\.slam.index",
        "decks": {
            "71634fe6-3a6a-4c24-9fa3-9c24c75ce066": {
                "cards": [
                    "d5983c7a-bea3-48dd-becb-3e683f2aed77",
                    "9edd6176-6881-4fab-aea8-8eb25186db03",
                    "ee1e58c2-df54-463a-b8dd-67f464b7b129",
                    "bdf3bee3-1e61-4f1b-b12c-caa59c7b4c06"
                ],
                "name": ""
            },
            "a7822006-f37a-4b89-867c-e876dd756383": {
                "cards": [
                    "91e9fcc0-b645-46ce-b3aa-ad94a2d7908d"
                ],
                "name": ""
            },
            "bbee818e-a85c-4fbd-85c8-f8d7b5382bb7": {
                "cards": [
                    "d5983c7a-bea3-48dd-becb-3e683f2aed77",
                    "9edd6176-6881-4fab-aea8-8eb25186db03"
                ],
                "name": ""
            }
        },
        "cards": {
            "91e9fcc0-b645-46ce-b3aa-ad94a2d7908d": {
                "model": {
                    "layout": {
                        "panes": [
                            {
                                "pane": {
                                    "panes": [
                                        {
                                            "pane": {
                                                "value": "bbee818e-a85c-4fbd-85c8-f8d7b5382bb7",
                                                "type": "cell"
                                            },
                                            "ratio": [
                                                1,
                                                1
                                            ]
                                        }
                                    ],
                                    "orientation": "horizontal",
                                    "type": "split"
                                },
                                "ratio": [
                                    1,
                                    2
                                ]
                            },
                            {
                                "pane": {
                                    "panes": [
                                        {
                                            "pane": {
                                                "value": "71634fe6-3a6a-4c24-9fa3-9c24c75ce066",
                                                "type": "cell"
                                            },
                                            "ratio": [
                                                1,
                                                1
                                            ]
                                        }
                                    ],
                                    "orientation": "horizontal",
                                    "type": "split"
                                },
                                "ratio": [
                                    1,
                                    2
                                ]
                            }
                        ],
                        "orientation": "vertical",
                        "type": "split"
                    }
                },
                "cardType": "draftboard"
            },
            "9edd6176-6881-4fab-aea8-8eb25186db03": {
                "model": {
                    "state": {
                        "Tool": {
                            "labels": {
                                "value": [
                                    {
                                        "literal": "all"
                                    },
                                    {
                                        "literal": "Argus"
                                    },
                                    {
                                        "literal": "Reconciliation"
                                    },
                                    {
                                        "literal": "Stuck Order Report"
                                    },
                                    {
                                        "literal": "Stuck Order Aging Report"
                                    },
                                    {
                                        "literal": "jTrace"
                                    },
                                    {
                                        "literal": "Stuck Order Error Report"
                                    },
                                    {
                                        "literal": "Collection Queue Report"
                                    },
                                    {
                                        "literal": "Krrish"
                                    },
                                    {
                                        "literal": "Ginger"
                                    },
                                    {
                                        "literal": "BAP Error Report"
                                    },
                                    {
                                        "literal": "TRB Error Report"
                                    },
                                    {
                                        "literal": "Usage Hourly Processing Statistic"
                                    },
                                    {
                                        "literal": "TC Monitoring Throughput Error Report"
                                    },
                                    {
                                        "literal": "Interaction Case Count Report"
                                    },
                                    {
                                        "literal": "Collection Roundtrip"
                                    },
                                    {
                                        "literal": "Collection Status Kpi"
                                    },
                                    {
                                        "literal": "Rated Events and PI Mismatch Report"
                                    },
                                    {
                                        "literal": "BCC Health Check Report"
                                    },
                                    {
                                        "literal": "Order Action Status"
                                    },
                                    {
                                        "literal": "Probe Order"
                                    },
                                    {
                                        "literal": "Collection Request Automation"
                                    },
                                    {
                                        "literal": "Usage Recon Daily Extract"
                                    },
                                    {
                                        "literal": "TRB Main Map"
                                    },
                                    {
                                        "literal": "AC Rebuild Map"
                                    },
                                    {
                                        "literal": "GSS EAAS BE"
                                    },
                                    {
                                        "literal": "Distributed Environment Installation"
                                    },
                                    {
                                        "literal": "Log Pattern Search Report"
                                    },
                                    {
                                        "literal": "Satellite Templates"
                                    },
                                    {
                                        "literal": "Long Running Queries"
                                    },
                                    {
                                        "literal": "Deployment Manager"
                                    },
                                    {
                                        "literal": "CopyBAN Self Service"
                                    },
                                    {
                                        "literal": "Junk Character Validation"
                                    },
                                    {
                                        "literal": "DB Compare Script"
                                    },
                                    {
                                        "literal": "Cancel Old Pending Orders"
                                    },
                                    {
                                        "literal": "One Click Billing"
                                    },
                                    {
                                        "literal": "SpyStudio"
                                    },
                                    {
                                        "literal": "BAP Failed Transaction Processing"
                                    },
                                    {
                                        "literal": "TRB Recycle"
                                    },
                                    {
                                        "literal": "BI Dashboard ETL"
                                    },
                                    {
                                        "literal": "BI Dashboard UI"
                                    },
                                    {
                                        "literal": "Unified Operations Console"
                                    },
                                    {
                                        "literal": "Elasticsearch"
                                    },
                                    {
                                        "literal": "Bill Cycle Summary Report"
                                    },
                                    {
                                        "literal": "NGM OM Agent"
                                    },
                                    {
                                        "literal": "Ansible"
                                    },
                                    {
                                        "literal": "Kibana"
                                    },
                                    {
                                        "literal": "Beats"
                                    },
                                    {
                                        "literal": "Logstash"
                                    },
                                    {
                                        "literal": "DB HF Verification"
                                    },
                                    {
                                        "literal": "XPack"
                                    },
                                    {
                                        "literal": "Oracle Empty Database Creation"
                                    },
                                    {
                                        "literal": "Amdocs Data Loader"
                                    },
                                    {
                                        "literal": "DB Incremental Apply"
                                    },
                                    {
                                        "literal": "Prepaid TC Monitoring"
                                    },
                                    {
                                        "literal": "DB Session Check"
                                    },
                                    {
                                        "literal": "Usage Success Rates"
                                    },
                                    {
                                        "literal": "Production Reports"
                                    },
                                    {
                                        "literal": "Usage throughput and error"
                                    },
                                    {
                                        "literal": "Telegraf Agent"
                                    },
                                    {
                                        "literal": "HP Diagnostics Probe"
                                    },
                                    {
                                        "literal": "Refund Recon"
                                    },
                                    {
                                        "literal": "Direct Debit Recon"
                                    },
                                    {
                                        "literal": "MCO"
                                    },
                                    {
                                        "literal": "Real Time Monitoring"
                                    },
                                    {
                                        "literal": "HP Diagnostic Server"
                                    },
                                    {
                                        "literal": "OMS Data Issue Analysis"
                                    },
                                    {
                                        "literal": "Usage Freshness"
                                    },
                                    {
                                        "literal": "MCO Templates"
                                    },
                                    {
                                        "literal": "MFS DB Archive"
                                    },
                                    {
                                        "literal": "Minions"
                                    },
                                    {
                                        "literal": "nmnbm"
                                    },
                                    {
                                        "literal": "bdbd"
                                    },
                                    {
                                        "literal": "qwerty"
                                    },
                                    {
                                        "literal": "Gin1"
                                    },
                                    {
                                        "literal": "Ginna"
                                    },
                                    {
                                        "literal": "Test0YF1S7"
                                    },
                                    {
                                        "literal": "SASS"
                                    },
                                    {
                                        "literal": "TOOL1"
                                    },
                                    {
                                        "literal": "SSS"
                                    },
                                    {
                                        "literal": "test1"
                                    },
                                    {
                                        "literal": "ok"
                                    },
                                    {
                                        "literal": "Test833"
                                    },
                                    {
                                        "literal": "TestSahil"
                                    },
                                    {
                                        "literal": "newTool"
                                    },
                                    {
                                        "literal": "ATOOLISSUE"
                                    },
                                    {
                                        "literal": "TOOLER"
                                    }
                                ],
                                "type": "lit"
                            },
                            "selection": {
                                "value": {
                                    "literal": "all"
                                },
                                "type": "lit"
                            },
                            "type": "dropdown"
                        },
                        "endDate": {
                            "textBox": {
                                "value": {
                                    "value": {
                                        "day": 1,
                                        "month": 1,
                                        "year": 2050
                                    },
                                    "type": "lit"
                                },
                                "type": "date"
                            },
                            "type": "textbox"
                        },
                        "beginDate": {
                            "textBox": {
                                "value": {
                                    "value": {
                                        "day": 1,
                                        "month": 1,
                                        "year": 2016
                                    },
                                    "type": "lit"
                                },
                                "type": "date"
                            },
                            "type": "textbox"
                        }
                    },
                    "input": {
                        "blocks": [
                            {
                                "content": [
                                    {
                                        "value": "Report",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "to",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "find",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "all",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "machines",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "on",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "which",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "the",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "Tool",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "is",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "Deployed:",
                                        "type": "str"
                                    }
                                ],
                                "level": 1,
                                "type": "header"
                            },
                            {
                                "content": [
                                    {
                                        "value": "Please",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "select",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "a",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "Tool:",
                                        "type": "str"
                                    }
                                ],
                                "level": 3,
                                "type": "header"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "labels": {
                                                "value": [
                                                    {
                                                        "literal": "all"
                                                    },
                                                    {
                                                        "literal": "Argus"
                                                    },
                                                    {
                                                        "literal": "Reconciliation"
                                                    },
                                                    {
                                                        "literal": "Stuck Order Report"
                                                    },
                                                    {
                                                        "literal": "Stuck Order Aging Report"
                                                    },
                                                    {
                                                        "literal": "jTrace"
                                                    },
                                                    {
                                                        "literal": "Stuck Order Error Report"
                                                    },
                                                    {
                                                        "literal": "Collection Queue Report"
                                                    },
                                                    {
                                                        "literal": "Krrish"
                                                    },
                                                    {
                                                        "literal": "Ginger"
                                                    },
                                                    {
                                                        "literal": "BAP Error Report"
                                                    },
                                                    {
                                                        "literal": "TRB Error Report"
                                                    },
                                                    {
                                                        "literal": "Usage Hourly Processing Statistic"
                                                    },
                                                    {
                                                        "literal": "TC Monitoring Throughput Error Report"
                                                    },
                                                    {
                                                        "literal": "Interaction Case Count Report"
                                                    },
                                                    {
                                                        "literal": "Collection Roundtrip"
                                                    },
                                                    {
                                                        "literal": "Collection Status Kpi"
                                                    },
                                                    {
                                                        "literal": "Rated Events and PI Mismatch Report"
                                                    },
                                                    {
                                                        "literal": "BCC Health Check Report"
                                                    },
                                                    {
                                                        "literal": "Order Action Status"
                                                    },
                                                    {
                                                        "literal": "Probe Order"
                                                    },
                                                    {
                                                        "literal": "Collection Request Automation"
                                                    },
                                                    {
                                                        "literal": "Usage Recon Daily Extract"
                                                    },
                                                    {
                                                        "literal": "TRB Main Map"
                                                    },
                                                    {
                                                        "literal": "AC Rebuild Map"
                                                    },
                                                    {
                                                        "literal": "GSS EAAS BE"
                                                    },
                                                    {
                                                        "literal": "Distributed Environment Installation"
                                                    },
                                                    {
                                                        "literal": "Log Pattern Search Report"
                                                    },
                                                    {
                                                        "literal": "Satellite Templates"
                                                    },
                                                    {
                                                        "literal": "Long Running Queries"
                                                    },
                                                    {
                                                        "literal": "Deployment Manager"
                                                    },
                                                    {
                                                        "literal": "CopyBAN Self Service"
                                                    },
                                                    {
                                                        "literal": "Junk Character Validation"
                                                    },
                                                    {
                                                        "literal": "DB Compare Script"
                                                    },
                                                    {
                                                        "literal": "Cancel Old Pending Orders"
                                                    },
                                                    {
                                                        "literal": "One Click Billing"
                                                    },
                                                    {
                                                        "literal": "SpyStudio"
                                                    },
                                                    {
                                                        "literal": "BAP Failed Transaction Processing"
                                                    },
                                                    {
                                                        "literal": "TRB Recycle"
                                                    },
                                                    {
                                                        "literal": "BI Dashboard ETL"
                                                    },
                                                    {
                                                        "literal": "BI Dashboard UI"
                                                    },
                                                    {
                                                        "literal": "Unified Operations Console"
                                                    },
                                                    {
                                                        "literal": "Elasticsearch"
                                                    },
                                                    {
                                                        "literal": "Bill Cycle Summary Report"
                                                    },
                                                    {
                                                        "literal": "NGM OM Agent"
                                                    },
                                                    {
                                                        "literal": "Ansible"
                                                    },
                                                    {
                                                        "literal": "Kibana"
                                                    },
                                                    {
                                                        "literal": "Beats"
                                                    },
                                                    {
                                                        "literal": "Logstash"
                                                    },
                                                    {
                                                        "literal": "DB HF Verification"
                                                    },
                                                    {
                                                        "literal": "XPack"
                                                    },
                                                    {
                                                        "literal": "Oracle Empty Database Creation"
                                                    },
                                                    {
                                                        "literal": "Amdocs Data Loader"
                                                    },
                                                    {
                                                        "literal": "DB Incremental Apply"
                                                    },
                                                    {
                                                        "literal": "Prepaid TC Monitoring"
                                                    },
                                                    {
                                                        "literal": "DB Session Check"
                                                    },
                                                    {
                                                        "literal": "Usage Success Rates"
                                                    },
                                                    {
                                                        "literal": "Production Reports"
                                                    },
                                                    {
                                                        "literal": "Usage throughput and error"
                                                    },
                                                    {
                                                        "literal": "Telegraf Agent"
                                                    },
                                                    {
                                                        "literal": "HP Diagnostics Probe"
                                                    },
                                                    {
                                                        "literal": "Refund Recon"
                                                    },
                                                    {
                                                        "literal": "Direct Debit Recon"
                                                    },
                                                    {
                                                        "literal": "MCO"
                                                    },
                                                    {
                                                        "literal": "Real Time Monitoring"
                                                    },
                                                    {
                                                        "literal": "HP Diagnostic Server"
                                                    },
                                                    {
                                                        "literal": "OMS Data Issue Analysis"
                                                    },
                                                    {
                                                        "literal": "Usage Freshness"
                                                    },
                                                    {
                                                        "literal": "MCO Templates"
                                                    },
                                                    {
                                                        "literal": "MFS DB Archive"
                                                    },
                                                    {
                                                        "literal": "Minions"
                                                    },
                                                    {
                                                        "literal": "nmnbm"
                                                    },
                                                    {
                                                        "literal": "bdbd"
                                                    },
                                                    {
                                                        "literal": "qwerty"
                                                    },
                                                    {
                                                        "literal": "Gin1"
                                                    },
                                                    {
                                                        "literal": "Ginna"
                                                    },
                                                    {
                                                        "literal": "Test0YF1S7"
                                                    },
                                                    {
                                                        "literal": "SASS"
                                                    },
                                                    {
                                                        "literal": "TOOL1"
                                                    },
                                                    {
                                                        "literal": "SSS"
                                                    },
                                                    {
                                                        "literal": "test1"
                                                    },
                                                    {
                                                        "literal": "ok"
                                                    },
                                                    {
                                                        "literal": "Test833"
                                                    },
                                                    {
                                                        "literal": "TestSahil"
                                                    },
                                                    {
                                                        "literal": "newTool"
                                                    },
                                                    {
                                                        "literal": "ATOOLISSUE"
                                                    },
                                                    {
                                                        "literal": "TOOLER"
                                                    }
                                                ],
                                                "type": "lit"
                                            },
                                            "selection": {
                                                "value": {
                                                    "literal": "all"
                                                },
                                                "type": "lit"
                                            },
                                            "type": "dropdown"
                                        },
                                        "required": False,
                                        "label": "Tool",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "textBox": {
                                                "value": {
                                                    "value": {
                                                        "day": 1,
                                                        "month": 1,
                                                        "year": 2016
                                                    },
                                                    "type": "lit"
                                                },
                                                "type": "date"
                                            },
                                            "type": "textbox"
                                        },
                                        "required": False,
                                        "label": "beginDate",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "textBox": {
                                                "value": {
                                                    "value": {
                                                        "day": 1,
                                                        "month": 1,
                                                        "year": 2050
                                                    },
                                                    "type": "lit"
                                                },
                                                "type": "date"
                                            },
                                            "type": "textbox"
                                        },
                                        "required": False,
                                        "label": "endDate",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            }
                        ],
                        "doc": "slamdown"
                    }
                },
                "cardType": "markdown"
            },
            "bdf3bee3-1e61-4f1b-b12c-caa59c7b4c06": {
                "model": {
                    "pageSize": 50,
                    "page": None
                },
                "cardType": "table"
            },
            "d5983c7a-bea3-48dd-becb-3e683f2aed77": {
                "model": {
                    "ranges": [],
                    "text": "# Report to find all machines on which the Tool is Deployed:\n\n### Please select a Tool:\n\nTool = {!``select name from `/DPM/DeploymentManager/Tool` order by name ``} (all)\n\nbeginDate = ____-__-__(2016-01-01)\n\nendDate = ____-__-__(2050-01-01)"
                },
                "cardType": "ace-markdown"
            },
            "ee1e58c2-df54-463a-b8dd-67f464b7b129": {
                "model": {
                    "ranges": [],
                    "text": "select m.machine_name as Machine, t.build_no as Build_No,v.version_name||\" \"||v.version_number as Version, tl.name as Tool_Name from `/DPM/DeploymentManager/ToolsOnMachine` as t\r\njoin `/DPM/DeploymentManager/Versions` as v on oid(t.parent_entity_id)=v._id\r\njoin `/DPM/DeploymentManager/Tool` as tl on oid(v.tool_id)=tl._id and tl.name = ( case when :Tool = \"all\" then tl.name else :Tool end )\r\njoin `/DPM/DeploymentManager/Machine` as m on oid(t.machine_id) = m._id  group by m.machine_name,v.tool_id order by tl.name asc, m.machine_name asc , t.Build_No desc "
                },
                "cardType": "ace-sql"
            }
        },
        "rootId": "a7822006-f37a-4b89-867c-e876dd756383",
        "version": 2

    }, {
        "collection_name": "Reports.DU_Deployment_History\.slam.index",
        "decks": {
            "66778e1f-5c61-4f2d-989a-5a95c990996b": {
                "cards": [
                    "446a4ab2-b3a0-454d-b5f0-6fa761faa107"
                ],
                "name": ""
            },
            "67734f12-cde9-4bfe-84dd-4062d77f4697": {
                "cards": [
                    "08920cc5-f269-4405-9128-9907faccb25d",
                    "4780c60e-522b-4b2f-a40a-329ce4359894",
                    "ae331e35-7afe-4ec5-aa92-08573af3da74",
                    "8ca6d8a7-1a65-4e51-b4a4-7fdfbcb19dc4"
                ],
                "name": ""
            },
            "6de6fdf2-6589-4532-9c05-ac97497e5fe7": {
                "cards": [
                    "08920cc5-f269-4405-9128-9907faccb25d",
                    "4780c60e-522b-4b2f-a40a-329ce4359894"
                ],
                "name": ""
            }
        },
        "cards": {
            "08920cc5-f269-4405-9128-9907faccb25d": {
                "model": {
                    "ranges": [],
                    "text": "# Select the DeploymentUnit and Machine to find delpoyment history\n\nDu = {!`` select name from `/DPM/DeploymentManager/DeploymentUnit` order by name ``}\n\nMachine = {!`` select machine_name from `/DPM/DeploymentManager/Machine` order by machine_name ``}\n\n\n"
                },
                "cardType": "ace-markdown"
            },
            "446a4ab2-b3a0-454d-b5f0-6fa761faa107": {
                "model": {
                    "layout": {
                        "panes": [
                            {
                                "pane": {
                                    "panes": [
                                        {
                                            "pane": {
                                                "value": "6de6fdf2-6589-4532-9c05-ac97497e5fe7",
                                                "type": "cell"
                                            },
                                            "ratio": [
                                                1,
                                                1
                                            ]
                                        }
                                    ],
                                    "orientation": "horizontal",
                                    "type": "split"
                                },
                                "ratio": [
                                    1,
                                    2
                                ]
                            },
                            {
                                "pane": {
                                    "panes": [
                                        {
                                            "pane": {
                                                "value": "67734f12-cde9-4bfe-84dd-4062d77f4697",
                                                "type": "cell"
                                            },
                                            "ratio": [
                                                1,
                                                1
                                            ]
                                        }
                                    ],
                                    "orientation": "horizontal",
                                    "type": "split"
                                },
                                "ratio": [
                                    1,
                                    2
                                ]
                            }
                        ],
                        "orientation": "vertical",
                        "type": "split"
                    }
                },
                "cardType": "draftboard"
            },
            "4780c60e-522b-4b2f-a40a-329ce4359894": {
                "model": {
                    "state": {
                        "Du": {
                            "labels": {
                                "value": [
                                    {
                                        "literal": "DU AR version 823"
                                    },
                                    {
                                        "literal": "DU AR version 825"
                                    },
                                    {
                                        "literal": "DU CM version 823"
                                    },
                                    {
                                        "literal": "DU CM version 825"
                                    },
                                    {
                                        "literal": "DU RPL version 825"
                                    },
                                    {
                                        "literal": "DU TC 825"
                                    }
                                ],
                                "type": "lit"
                            },
                            "selection": {
                                "value": {
                                    "literal": "DU AR version 825"
                                },
                                "type": "lit"
                            },
                            "type": "dropdown"
                        },
                        "Machine": {
                            "labels": {
                                "value": [
                                    {
                                        "literal": "pcmwl11@10.30.134.86"
                                    },
                                    {
                                        "literal": "pxlcrb11@10.30.134.79"
                                    },
                                    {
                                        "literal": "root@illin4489"
                                    },
                                    {
                                        "literal": "uatabp11@10.30.134.89"
                                    },
                                    {
                                        "literal": "uatabp22@10.30.134.90"
                                    },
                                    {
                                        "literal": "uatabp22edpm@10.30.134.90"
                                    },
                                    {
                                        "literal": "uatabp25@10.30.134.90"
                                    },
                                    {
                                        "literal": "uatabp8@10.30.134.89"
                                    },
                                    {
                                        "literal": "uatabp8edpm@10.30.134.89"
                                    },
                                    {
                                        "literal": "vptool@10.30.149.133"
                                    }
                                ],
                                "type": "lit"
                            },
                            "selection": {
                                "value": {
                                    "literal": "uatabp22edpm@10.30.134.90"
                                },
                                "type": "lit"
                            },
                            "type": "dropdown"
                        }
                    },
                    "input": {
                        "blocks": [
                            {
                                "content": [
                                    {
                                        "value": "Select",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "the",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "DeploymentUnit",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "and",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "Machine",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "to",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "find",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "delpoyment",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "history",
                                        "type": "str"
                                    }
                                ],
                                "level": 1,
                                "type": "header"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "labels": {
                                                "value": [
                                                    {
                                                        "literal": "DU AR version 823"
                                                    },
                                                    {
                                                        "literal": "DU AR version 825"
                                                    },
                                                    {
                                                        "literal": "DU CM version 823"
                                                    },
                                                    {
                                                        "literal": "DU CM version 825"
                                                    },
                                                    {
                                                        "literal": "DU RPL version 825"
                                                    },
                                                    {
                                                        "literal": "DU TC 825"
                                                    }
                                                ],
                                                "type": "lit"
                                            },
                                            "selection": None,
                                            "type": "dropdown"
                                        },
                                        "required": False,
                                        "label": "Du",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "labels": {
                                                "value": [
                                                    {
                                                        "literal": "pcmwl11@10.30.134.86"
                                                    },
                                                    {
                                                        "literal": "pxlcrb11@10.30.134.79"
                                                    },
                                                    {
                                                        "literal": "root@illin4489"
                                                    },
                                                    {
                                                        "literal": "uatabp11@10.30.134.89"
                                                    },
                                                    {
                                                        "literal": "uatabp22@10.30.134.90"
                                                    },
                                                    {
                                                        "literal": "uatabp22edpm@10.30.134.90"
                                                    },
                                                    {
                                                        "literal": "uatabp25@10.30.134.90"
                                                    },
                                                    {
                                                        "literal": "uatabp8@10.30.134.89"
                                                    },
                                                    {
                                                        "literal": "uatabp8edpm@10.30.134.89"
                                                    },
                                                    {
                                                        "literal": "vptool@10.30.149.133"
                                                    }
                                                ],
                                                "type": "lit"
                                            },
                                            "selection": None,
                                            "type": "dropdown"
                                        },
                                        "required": False,
                                        "label": "Machine",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            }
                        ],
                        "doc": "slamdown"
                    }
                },
                "cardType": "markdown"
            },
            "8ca6d8a7-1a65-4e51-b4a4-7fdfbcb19dc4": {
                "model": {
                    "pageSize": None,
                    "page": None
                },
                "cardType": "table"
            },
            "ae331e35-7afe-4ec5-aa92-08573af3da74": {
                "model": {
                    "ranges": [],
                    "text": "select t.requested_by as RequestedBy,t.request_type as DeploymentType,t.update_date as DeploymentDate, t.build_number \r\nfrom `/DPM/DeploymentManager/DeploymentRequest` as t\r\njoin `/DPM/DeploymentManager/DeploymentUnit` as du\r\non oid(t.parent_entity_id)=du._id and du.name=:Du \r\njoin `/DPM/DeploymentManager/Machine` as m \r\non oid(t.machine_id) = m._id  and m.machine_name=:Machine\r\norder by t.update_date desc"
                },
                "cardType": "ace-sql"
            }
        },
        "rootId": "66778e1f-5c61-4f2d-989a-5a95c990996b",
        "version": 2
    },
    {
        "collection_name": "Reports.Tool_Deployment_History\.slam.index",
        "decks": {
            "0223a268-dc20-43ec-9436-8fef016459b4": {
                "cards": [
                    "0d48a462-f846-4a69-8aa3-6b8af203f7ee",
                    "b182fc9f-b76c-4960-b5c3-e0044a15ec14"
                ],
                "name": ""
            },
            "a9d869b8-b98c-44b6-9b91-fe32123df1f4": {
                "cards": [
                    "0d48a462-f846-4a69-8aa3-6b8af203f7ee",
                    "b182fc9f-b76c-4960-b5c3-e0044a15ec14",
                    "46beafd9-9fbb-4a87-8ced-fa59475c84f1",
                    "f9f8a4fe-d35f-4def-b05b-37eae77c6a63"
                ],
                "name": ""
            },
            "fe7ad867-8553-41b0-a871-9c2eeb41bd88": {
                "cards": [
                    "3a0c41f6-8af6-49cd-aeab-0cab106ffef8"
                ],
                "name": ""
            }
        },
        "cards": {
            "0d48a462-f846-4a69-8aa3-6b8af203f7ee": {
                "model": {
                    "ranges": [],
                    "text": "# Select the Tool and Machine to find delpoyment history\n\nToolName = {!`` select name from `/DPM/DeploymentManager/Tool` order by name ``}\n\nMachine = {!`` select machine_name from `/DPM/DeploymentManager/Machine` order by machine_name ``}\n\n\n"
                },
                "cardType": "ace-markdown"
            },
            "3a0c41f6-8af6-49cd-aeab-0cab106ffef8": {
                "model": {
                    "layout": {
                        "panes": [
                            {
                                "pane": {
                                    "panes": [
                                        {
                                            "pane": {
                                                "value": "0223a268-dc20-43ec-9436-8fef016459b4",
                                                "type": "cell"
                                            },
                                            "ratio": [
                                                1,
                                                1
                                            ]
                                        }
                                    ],
                                    "orientation": "horizontal",
                                    "type": "split"
                                },
                                "ratio": [
                                    1,
                                    2
                                ]
                            },
                            {
                                "pane": {
                                    "panes": [
                                        {
                                            "pane": {
                                                "value": "a9d869b8-b98c-44b6-9b91-fe32123df1f4",
                                                "type": "cell"
                                            },
                                            "ratio": [
                                                1,
                                                1
                                            ]
                                        }
                                    ],
                                    "orientation": "horizontal",
                                    "type": "split"
                                },
                                "ratio": [
                                    1,
                                    2
                                ]
                            }
                        ],
                        "orientation": "vertical",
                        "type": "split"
                    }
                },
                "cardType": "draftboard"
            },
            "46beafd9-9fbb-4a87-8ced-fa59475c84f1": {
                "model": {
                    "ranges": [],
                    "text": "select t.requested_by as RequestedBy,t.request_type as DeploymentType,t.update_date as DeploymentDate, t.build_number \r\nfrom `/DPM/DeploymentManager/DeploymentRequest` as t\r\njoin `/DPM/DeploymentManager/Versions` as v\r\non oid(t.parent_entity_id)=v._id \r\njoin `/DPM/DeploymentManager/Tool` as tool\r\non oid(v.tool_id)=tool._id\r\njoin `/DPM/DeploymentManager/Machine` as m \r\non oid(t.machine_id) = m._id  and m.machine_name=:Machine\r\norder by t.update_date desc\r\n"
                },
                "cardType": "ace-sql"
            },
            "b182fc9f-b76c-4960-b5c3-e0044a15ec14": {
                "model": {
                    "state": {
                        "ToolName": {
                            "labels": {
                                "value": [
                                    {
                                        "literal": "Argus"
                                    },
                                    {
                                        "literal": "Beats"
                                    },
                                    {
                                        "literal": "Bill Cycle Summary Report"
                                    },
                                    {
                                        "literal": "Collection Queue Report"
                                    },
                                    {
                                        "literal": "Collection Request Automation"
                                    },
                                    {
                                        "literal": "Collection Roundtrip"
                                    },
                                    {
                                        "literal": "Collection Status Kpi"
                                    },
                                    {
                                        "literal": "DAM Digital Analytics  Monitoring"
                                    },
                                    {
                                        "literal": "ESstack"
                                    },
                                    {
                                        "literal": "Elasticsearch"
                                    },
                                    {
                                        "literal": "Kibana"
                                    },
                                    {
                                        "literal": "Krrish"
                                    },
                                    {
                                        "literal": "Logstash"
                                    },
                                    {
                                        "literal": "Postpaid Dashboard"
                                    },
                                    {
                                        "literal": "RPLDASHBOARD"
                                    },
                                    {
                                        "literal": "Rated Events and PI Mismatch Report"
                                    },
                                    {
                                        "literal": "Reconciliation"
                                    },
                                    {
                                        "literal": "TCJUPITEROPSDASH"
                                    },
                                    {
                                        "literal": "TRB Error Report"
                                    },
                                    {
                                        "literal": "TRB Recycle"
                                    },
                                    {
                                        "literal": "TcExplorer"
                                    },
                                    {
                                        "literal": "Test"
                                    },
                                    {
                                        "literal": "Touch Free Product Catalogue Deployer"
                                    },
                                    {
                                        "literal": "UXF Dashboard"
                                    },
                                    {
                                        "literal": "Usage Hourly Processing Statistic"
                                    },
                                    {
                                        "literal": "Usage Recon Daily Extract"
                                    },
                                    {
                                        "literal": "jTrace"
                                    },
                                    {
                                        "literal": "jTraceIMPL"
                                    },
                                    {
                                        "literal": "subscrdetail"
                                    }
                                ],
                                "type": "lit"
                            },
                            "selection": {
                                "value": {
                                    "literal": "Argus"
                                },
                                "type": "lit"
                            },
                            "type": "dropdown"
                        },
                        "Machine": {
                            "labels": {
                                "value": [
                                    {
                                        "literal": "pcmwl11@10.30.134.86"
                                    },
                                    {
                                        "literal": "pxlcrb11@10.30.134.79"
                                    },
                                    {
                                        "literal": "root@illin4489"
                                    },
                                    {
                                        "literal": "uatabp11@10.30.134.89"
                                    },
                                    {
                                        "literal": "uatabp22@10.30.134.90"
                                    },
                                    {
                                        "literal": "uatabp22edpm@10.30.134.90"
                                    },
                                    {
                                        "literal": "uatabp25@10.30.134.90"
                                    },
                                    {
                                        "literal": "uatabp8@10.30.134.89"
                                    },
                                    {
                                        "literal": "uatabp8edpm@10.30.134.89"
                                    },
                                    {
                                        "literal": "vptool@10.30.149.133"
                                    }
                                ],
                                "type": "lit"
                            },
                            "selection": {
                                "value": {
                                    "literal": "pcmwl11@10.30.134.86"
                                },
                                "type": "lit"
                            },
                            "type": "dropdown"
                        }
                    },
                    "input": {
                        "blocks": [
                            {
                                "content": [
                                    {
                                        "value": "Select",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "the",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "Tool",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "and",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "Machine",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "to",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "find",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "delpoyment",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "history",
                                        "type": "str"
                                    }
                                ],
                                "level": 1,
                                "type": "header"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "labels": {
                                                "value": [
                                                    {
                                                        "literal": "Argus"
                                                    },
                                                    {
                                                        "literal": "Beats"
                                                    },
                                                    {
                                                        "literal": "Bill Cycle Summary Report"
                                                    },
                                                    {
                                                        "literal": "Collection Queue Report"
                                                    },
                                                    {
                                                        "literal": "Collection Request Automation"
                                                    },
                                                    {
                                                        "literal": "Collection Roundtrip"
                                                    },
                                                    {
                                                        "literal": "Collection Status Kpi"
                                                    },
                                                    {
                                                        "literal": "DAM Digital Analytics  Monitoring"
                                                    },
                                                    {
                                                        "literal": "ESstack"
                                                    },
                                                    {
                                                        "literal": "Elasticsearch"
                                                    },
                                                    {
                                                        "literal": "Kibana"
                                                    },
                                                    {
                                                        "literal": "Krrish"
                                                    },
                                                    {
                                                        "literal": "Logstash"
                                                    },
                                                    {
                                                        "literal": "Postpaid Dashboard"
                                                    },
                                                    {
                                                        "literal": "RPLDASHBOARD"
                                                    },
                                                    {
                                                        "literal": "Rated Events and PI Mismatch Report"
                                                    },
                                                    {
                                                        "literal": "Reconciliation"
                                                    },
                                                    {
                                                        "literal": "TCJUPITEROPSDASH"
                                                    },
                                                    {
                                                        "literal": "TRB Error Report"
                                                    },
                                                    {
                                                        "literal": "TRB Recycle"
                                                    },
                                                    {
                                                        "literal": "TcExplorer"
                                                    },
                                                    {
                                                        "literal": "Test"
                                                    },
                                                    {
                                                        "literal": "Touch Free Product Catalogue Deployer"
                                                    },
                                                    {
                                                        "literal": "UXF Dashboard"
                                                    },
                                                    {
                                                        "literal": "Usage Hourly Processing Statistic"
                                                    },
                                                    {
                                                        "literal": "Usage Recon Daily Extract"
                                                    },
                                                    {
                                                        "literal": "jTrace"
                                                    },
                                                    {
                                                        "literal": "jTraceIMPL"
                                                    },
                                                    {
                                                        "literal": "subscrdetail"
                                                    }
                                                ],
                                                "type": "lit"
                                            },
                                            "selection": None,
                                            "type": "dropdown"
                                        },
                                        "required": False,
                                        "label": "ToolName",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "labels": {
                                                "value": [
                                                    {
                                                        "literal": "pcmwl11@10.30.134.86"
                                                    },
                                                    {
                                                        "literal": "pxlcrb11@10.30.134.79"
                                                    },
                                                    {
                                                        "literal": "root@illin4489"
                                                    },
                                                    {
                                                        "literal": "uatabp11@10.30.134.89"
                                                    },
                                                    {
                                                        "literal": "uatabp22@10.30.134.90"
                                                    },
                                                    {
                                                        "literal": "uatabp22edpm@10.30.134.90"
                                                    },
                                                    {
                                                        "literal": "uatabp25@10.30.134.90"
                                                    },
                                                    {
                                                        "literal": "uatabp8@10.30.134.89"
                                                    },
                                                    {
                                                        "literal": "uatabp8edpm@10.30.134.89"
                                                    },
                                                    {
                                                        "literal": "vptool@10.30.149.133"
                                                    }
                                                ],
                                                "type": "lit"
                                            },
                                            "selection": None,
                                            "type": "dropdown"
                                        },
                                        "required": False,
                                        "label": "Machine",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            }
                        ],
                        "doc": "slamdown"
                    }
                },
                "cardType": "markdown"
            },
            "f9f8a4fe-d35f-4def-b05b-37eae77c6a63": {
                "model": {
                    "pageSize": None,
                    "page": None
                },
                "cardType": "table"
            }
        },
        "rootId": "fe7ad867-8553-41b0-a871-9c2eeb41bd88",
        "version": 2
    }, {
        "collection_name": "Reports.Multiple_Dus_Deployed_On_Machine\.slam.index",
        "decks": {
            "57925a9f-7887-44e8-921b-0fc1f59efd7b": {
                "cards": [
                    "63d69bf3-1661-4d97-81ab-aa302bc273a2"
                ],
                "name": ""
            },
            "c2ef3bab-e44b-4d07-a46c-63fb847cbebe": {
                "cards": [
                    "90c82a9c-abf4-46cf-a62a-04c1475c309e",
                    "4b53ad63-cf91-43f4-903e-2cad126a9b60"
                ],
                "name": ""
            },
            "d98f038e-6ad2-4b12-a496-d4a979109739": {
                "cards": [
                    "90c82a9c-abf4-46cf-a62a-04c1475c309e",
                    "4b53ad63-cf91-43f4-903e-2cad126a9b60",
                    "16867c0d-e304-4116-859c-8b02810c2d50",
                    "c4dfd417-c0d3-4d71-a33a-dd4e81497d84"
                ],
                "name": ""
            }
        },
        "cards": {
            "16867c0d-e304-4116-859c-8b02810c2d50": {
                "model": {
                    "ranges": [],
                    "text": "select distinct (du.name) as DeploymentUnitName,m.machine_name as Machine, t.build_no as Build\r\nfrom `/DPM/DeploymentManager/ToolsOnMachine` as t\r\njoin `/DPM/DeploymentManager/DeploymentUnit` as du\r\non oid(t.parent_entity_id)=du._id\r\njoin `/DPM/DeploymentManager/Machine` as m\r\non oid(t.machine_id) = m._id and m.machine_name = (case when :Machine = \"all\" then m.machine_name else :Machine end)\r\ngroup by m.machine_name , du.name , t.build_no order by du.name asc,t.build_no desc  ,m.machine_name asc"
                },
                "cardType": "ace-sql"
            },
            "4b53ad63-cf91-43f4-903e-2cad126a9b60": {
                "model": {
                    "state": {
                        "Machine": {
                            "labels": {
                                "value": [
                                    {
                                        "literal": "all"
                                    },
                                    {
                                        "literal": "uatabp8@10.30.134.89"
                                    },
                                    {
                                        "literal": "uatabp22@10.30.134.90"
                                    },
                                    {
                                        "literal": "pxlcrb11@10.30.134.79"
                                    },
                                    {
                                        "literal": "vptool@10.30.149.133"
                                    },
                                    {
                                        "literal": "pcmwl11@10.30.134.86"
                                    },
                                    {
                                        "literal": "uatabp11@10.30.134.89"
                                    },
                                    {
                                        "literal": "root@illin4489"
                                    },
                                    {
                                        "literal": "uatabp8edpm@10.30.134.89"
                                    },
                                    {
                                        "literal": "uatabp22edpm@10.30.134.90"
                                    },
                                    {
                                        "literal": "uatabp25@10.30.134.90"
                                    }
                                ],
                                "type": "lit"
                            },
                            "selection": {
                                "value": {
                                    "literal": "all"
                                },
                                "type": "lit"
                            },
                            "type": "dropdown"
                        },
                        "beginDate": {
                            "textBox": {
                                "value": {
                                    "value": {
                                        "day": 1,
                                        "month": 1,
                                        "year": 2016
                                    },
                                    "type": "lit"
                                },
                                "type": "date"
                            },
                            "type": "textbox"
                        },
                        "endDate": {
                            "textBox": {
                                "value": {
                                    "value": {
                                        "day": 1,
                                        "month": 1,
                                        "year": 2050
                                    },
                                    "type": "lit"
                                },
                                "type": "date"
                            },
                            "type": "textbox"
                        }
                    },
                    "input": {
                        "blocks": [
                            {
                                "content": [
                                    {
                                        "value": "Select",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "Machine",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "to",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "find",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "all",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "DeploymentUnits",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "deployed",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "on",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "that",
                                        "type": "str"
                                    },
                                    {
                                        "type": "space"
                                    },
                                    {
                                        "value": "machine",
                                        "type": "str"
                                    }
                                ],
                                "level": 2,
                                "type": "header"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "labels": {
                                                "value": [
                                                    {
                                                        "literal": "all"
                                                    },
                                                    {
                                                        "literal": "uatabp8@10.30.134.89"
                                                    },
                                                    {
                                                        "literal": "uatabp22@10.30.134.90"
                                                    },
                                                    {
                                                        "literal": "pxlcrb11@10.30.134.79"
                                                    },
                                                    {
                                                        "literal": "vptool@10.30.149.133"
                                                    },
                                                    {
                                                        "literal": "pcmwl11@10.30.134.86"
                                                    },
                                                    {
                                                        "literal": "uatabp11@10.30.134.89"
                                                    },
                                                    {
                                                        "literal": "root@illin4489"
                                                    },
                                                    {
                                                        "literal": "uatabp8edpm@10.30.134.89"
                                                    },
                                                    {
                                                        "literal": "uatabp22edpm@10.30.134.90"
                                                    },
                                                    {
                                                        "literal": "uatabp25@10.30.134.90"
                                                    }
                                                ],
                                                "type": "lit"
                                            },
                                            "selection": {
                                                "value": {
                                                    "literal": "all"
                                                },
                                                "type": "lit"
                                            },
                                            "type": "dropdown"
                                        },
                                        "required": False,
                                        "label": "Machine",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "textBox": {
                                                "value": {
                                                    "value": {
                                                        "day": 1,
                                                        "month": 1,
                                                        "year": 2016
                                                    },
                                                    "type": "lit"
                                                },
                                                "type": "date"
                                            },
                                            "type": "textbox"
                                        },
                                        "required": False,
                                        "label": "beginDate",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            },
                            {
                                "content": [
                                    {
                                        "field": {
                                            "textBox": {
                                                "value": {
                                                    "value": {
                                                        "day": 1,
                                                        "month": 1,
                                                        "year": 2050
                                                    },
                                                    "type": "lit"
                                                },
                                                "type": "date"
                                            },
                                            "type": "textbox"
                                        },
                                        "required": False,
                                        "label": "endDate",
                                        "type": "field"
                                    }
                                ],
                                "type": "para"
                            }
                        ],
                        "doc": "slamdown"
                    }
                },
                "cardType": "markdown"
            },
            "63d69bf3-1661-4d97-81ab-aa302bc273a2": {
                "model": {
                    "layout": {
                        "panes": [
                            {
                                "pane": {
                                    "panes": [
                                        {
                                            "pane": {
                                                "value": "c2ef3bab-e44b-4d07-a46c-63fb847cbebe",
                                                "type": "cell"
                                            },
                                            "ratio": [
                                                1,
                                                1
                                            ]
                                        }
                                    ],
                                    "orientation": "horizontal",
                                    "type": "split"
                                },
                                "ratio": [
                                    1,
                                    2
                                ]
                            },
                            {
                                "pane": {
                                    "panes": [
                                        {
                                            "pane": {
                                                "value": "d98f038e-6ad2-4b12-a496-d4a979109739",
                                                "type": "cell"
                                            },
                                            "ratio": [
                                                1,
                                                1
                                            ]
                                        }
                                    ],
                                    "orientation": "horizontal",
                                    "type": "split"
                                },
                                "ratio": [
                                    1,
                                    2
                                ]
                            }
                        ],
                        "orientation": "vertical",
                        "type": "split"
                    }
                },
                "cardType": "draftboard"
            },
            "90c82a9c-abf4-46cf-a62a-04c1475c309e": {
                "model": {
                    "ranges": [],
                    "text": "## Select Machine to find all DeploymentUnits deployed on that machine\nMachine = {!``select machine_name from `/DPM/DeploymentManager/Machine` ``} (all)\n\nbeginDate = ____-__-__(2016-01-01)\n\nendDate = ____-__-__(2050-01-01)\n"
                },
                "cardType": "ace-markdown"
            },
            "c4dfd417-c0d3-4d71-a33a-dd4e81497d84": {
                "model": {
                    "pageSize": None,
                    "page": None
                },
                "cardType": "table"
            }
        },
        "rootId": "57925a9f-7887-44e8-921b-0fc1f59efd7b",
        "version": 2
    },{
       "collection_name": "Reports.DUPackage_Multi_State_View\.slam.index",
       "decks" : {
        "347ea5b9-1531-46b0-a029-69c0616c179e" : {
            "cards" : [
                "556f65e7-7ef3-452f-9200-b3002611f799", 
                "1da6d336-da29-4ce4-a1bd-d5c8b23f48ec"
            ], 
            "name" : ""
        }, 
        "8c0add71-fec4-4153-b96a-5dd0480c6f2e" : {
            "cards" : [
                "556f65e7-7ef3-452f-9200-b3002611f799", 
                "1da6d336-da29-4ce4-a1bd-d5c8b23f48ec", 
                "5c92f8b6-c9cf-4fbd-92d4-4eed8ef0e3a2", 
                "526fd1ce-9019-4f58-81db-9077f2be0962", 
                "6c71a330-ca9c-42d9-9200-fcc208bad7cf", 
                "b5b11402-31a7-43a7-96e9-b879999cccaa", 
                "0d952d5f-ad04-480f-9731-24ab57c98ebe", 
                "4d4b6cfb-e5a0-434c-9ec4-79fdbeefa621", 
                "1be7f9aa-78ba-4d3b-8444-1ce250fd6283", 
                "a8b45a27-7f78-46c3-98e4-34f59b556073"
            ], 
            "name" : ""
        }, 
        "ac5966a2-4377-4ff2-8170-3b96a127c435" : {
            "cards" : [
                "556f65e7-7ef3-452f-9200-b3002611f799", 
                "1da6d336-da29-4ce4-a1bd-d5c8b23f48ec", 
                "5c92f8b6-c9cf-4fbd-92d4-4eed8ef0e3a2", 
                "526fd1ce-9019-4f58-81db-9077f2be0962"
            ], 
            "name" : ""
        }, 
        "b1852407-91bb-425d-a826-c2c670500c84" : {
            "cards" : [
                "556f65e7-7ef3-452f-9200-b3002611f799", 
                "1da6d336-da29-4ce4-a1bd-d5c8b23f48ec", 
                "5c92f8b6-c9cf-4fbd-92d4-4eed8ef0e3a2", 
                "526fd1ce-9019-4f58-81db-9077f2be0962", 
                "6c71a330-ca9c-42d9-9200-fcc208bad7cf", 
                "b5b11402-31a7-43a7-96e9-b879999cccaa", 
                "0d952d5f-ad04-480f-9731-24ab57c98ebe", 
                "4d4b6cfb-e5a0-434c-9ec4-79fdbeefa621"
            ], 
            "name" : ""
        }, 
        "ccacf276-02d3-4b01-b5c8-9600c56c5eee" : {
            "cards" : [
                "556f65e7-7ef3-452f-9200-b3002611f799", 
                "1da6d336-da29-4ce4-a1bd-d5c8b23f48ec", 
                "5c92f8b6-c9cf-4fbd-92d4-4eed8ef0e3a2", 
                "526fd1ce-9019-4f58-81db-9077f2be0962", 
                "6c71a330-ca9c-42d9-9200-fcc208bad7cf", 
                "b5b11402-31a7-43a7-96e9-b879999cccaa"
            ], 
            "name" : ""
        }, 
        "f8306699-668e-414a-b3ca-78986afd7c58" : {
            "cards" : [
                "dcdfa4e9-5366-40aa-a3ec-054e7285e71b"
            ], 
            "name" : ""
        }
    }, 
    "cards" : {
        "0d952d5f-ad04-480f-9731-24ab57c98ebe" : {
            "model" : {
                "ranges" : [

                ], 
                "text" : "### Please select a Machine :\r\n\r\nMachine = {!`` select m.machine_name from `/DPM/DeploymentManager/Machine` as m join  `/DPM/DeploymentManager/MachineGroups` \r\nas mg on m._id = oid(mg.machine_id_list[*])  where  \r\nmg.group_name = :MachineGroup order by m.machine_name ``}(All)\r\n "
            }, 
            "cardType" : "ace-markdown"
        }, 
        "1be7f9aa-78ba-4d3b-8444-1ce250fd6283" : {
            "model" : {
                "ranges" : [

                ], 
                "text" : "select du1.name as DuName,s.name as PackageStateName, m.machine_name as MachineName,\r\ndr.build_number as BuildNo, dr.requested_by as RequestedBy ,\r\ndr.end_time as DeployedDate , dr.request_type as RequestType\r\nfrom (select * from `/DPM/DeploymentManager/DeploymentRequest` where package_state_id is not null AND skipped_ind is null) as dr \r\njoin `/DPM/DeploymentManager/DeploymentUnit`as du1 on oid(dr.parent_entity_id)= du1._id \r\njoin `/DPM/DeploymentManager/DeploymentUnitSet`as du on du.name= :DUPackage\r\njoin  `/DPM/DeploymentManager/State` as s on (oid(dr.package_state_id)= s._id and du._id = oid(s.parent_entity_id) and s.name = (case when :State  = \"All\" then s.name  else :State end) )\r\njoin  `/DPM/DeploymentManager/MachineGroups` as mg on ( (dr.machine_id) = mg.machine_id_list[*] and mg.group_name = :MachineGroup ) \r\njoin `/DPM/DeploymentManager/Machine` as m on (oid(dr.machine_id) = m._id and  \r\nm.machine_name = (case when :Machine  = \"All\" then  m.machine_name  else :Machine  end)) \r\nwhere  dr.package_state_id is not null\r\nAND LOWER(dr.deployment_type) = \"dugroup\" and LOWER(dr.status) = \"done\"\r\norder by du1.name , s.name"
            }, 
            "cardType" : "ace-sql"
        }, 
        "1da6d336-da29-4ce4-a1bd-d5c8b23f48ec" : {
            "model" : {
                "state" : {
                    "DUPackage" : {
                        "labels" : {
                            "value" : [
                                {
                                    "literal" : "DUPackage2"
                                }, 
                                {
                                    "literal" : "Test Du Package"
                                }
                            ], 
                            "type" : "lit"
                        }, 
                        "selection" : {
                            "value" : {
                                "literal" : "DUPackage2"
                            }, 
                            "type" : "lit"
                        }, 
                        "type" : "dropdown"
                    }
                }, 
                "input" : {
                    "blocks" : [
                        {
                            "content" : [
                                {
                                    "value" : [
                                        {
                                            "value" : "Report", 
                                            "type" : "str"
                                        }, 
                                        {
                                            "type" : "space"
                                        }, 
                                        {
                                            "value" : "for", 
                                            "type" : "str"
                                        }, 
                                        {
                                            "type" : "space"
                                        }, 
                                        {
                                            "value" : "Deployment", 
                                            "type" : "str"
                                        }, 
                                        {
                                            "type" : "space"
                                        }, 
                                        {
                                            "value" : "History", 
                                            "type" : "str"
                                        }, 
                                        {
                                            "type" : "space"
                                        }, 
                                        {
                                            "value" : "of", 
                                            "type" : "str"
                                        }, 
                                        {
                                            "type" : "space"
                                        }, 
                                        {
                                            "value" : "DUPackage", 
                                            "type" : "str"
                                        }
                                    ], 
                                    "type" : "strong"
                                }
                            ],
                            "level" : 1,
                            "type" : "header"
                        }, 
                        {
                            "content" : [
                                {
                                    "type" : "space"
                                }
                            ], 
                            "type" : "para"
                        }, 
                        {
                            "content" : [
                                {
                                    "value" : "Please", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "select", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "a", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "DUPackage", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : ":", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }
                            ],
                            "level" : 3,
                            "type" : "header"
                        }, 
                        {
                            "content" : [
                                {
                                    "type" : "softbreak"
                                }, 
                                {
                                    "field" : {
                                        "labels" : {
                                            "value" : [
                                                {
                                                    "literal" : "DUPackage2"
                                                }, 
                                                {
                                                    "literal" : "Test Du Package"
                                                }
                                            ], 
                                            "type" : "lit"
                                        },
                                        "selection" : None,
                                        "type" : "dropdown"
                                    },
                                    "required" : False,
                                    "label" : "DUPackage",
                                    "type" : "field"
                                }
                            ], 
                            "type" : "para"
                        }
                    ], 
                    "doc" : "slamdown"
                }
            }, 
            "cardType" : "markdown"
        }, 
        "4d4b6cfb-e5a0-434c-9ec4-79fdbeefa621" : {
            "model" : {
                "state" : {
                    "Machine" : {
                        "labels" : {
                            "value" : [
                                {
                                    "literal" : "All"
                                }, 
                                {
                                    "literal" : "root@indlin4610"
                                }, 
                                {
                                    "literal" : "root@vptestind011ghjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjghjhgjhgjhgj"
                                }
                            ], 
                            "type" : "lit"
                        }, 
                        "selection" : {
                            "value" : {
                                "literal" : "All"
                            }, 
                            "type" : "lit"
                        }, 
                        "type" : "dropdown"
                    }
                }, 
                "input" : {
                    "blocks" : [
                        {
                            "content" : [
                                {
                                    "value" : "Please", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "select", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "a", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "Machine", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : ":", 
                                    "type" : "str"
                                }
                            ],
                            "level" : 3,
                            "type" : "header"
                        }, 
                        {
                            "content" : [
                                {
                                    "type" : "softbreak"
                                }, 
                                {
                                    "field" : {
                                        "labels" : {
                                            "value" : [
                                                {
                                                    "literal" : "All"
                                                }, 
                                                {
                                                    "literal" : "root@indlin4610"
                                                }, 
                                                {
                                                    "literal" : "root@vptestind011ghjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjghjhgjhgjhgj"
                                                }
                                            ], 
                                            "type" : "lit"
                                        }, 
                                        "selection" : {
                                            "value" : {
                                                "literal" : "All"
                                            }, 
                                            "type" : "lit"
                                        }, 
                                        "type" : "dropdown"
                                    },
                                    "required" : False,
                                    "label" : "Machine",
                                    "type" : "field"
                                }, 
                                {
                                    "type" : "space"
                                }
                            ], 
                            "type" : "para"
                        }
                    ], 
                    "doc" : "slamdown"
                }
            }, 
            "cardType" : "markdown"
        }, 
        "526fd1ce-9019-4f58-81db-9077f2be0962" : {
            "model" : {
                "state" : {
                    "DUState" : {
                        "labels" : {
                            "value" : [
                                {
                                    "literal" : "All"
                                }, 
                                {
                                    "literal" : "Yo"
                                }, 
                                {
                                    "literal" : "Yo1"
                                }
                            ], 
                            "type" : "lit"
                        }, 
                        "selection" : {
                            "value" : {
                                "literal" : "All"
                            }, 
                            "type" : "lit"
                        }, 
                        "type" : "dropdown"
                    }
                }, 
                "input" : {
                    "blocks" : [
                        {
                            "content" : [
                                {
                                    "value" : "Please", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "select", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "a", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "DUPackageState", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : ":", 
                                    "type" : "str"
                                }
                            ],
                            "level" : 3,
                            "type" : "header"
                        }, 
                        {
                            "content" : [
                                {
                                    "type" : "softbreak"
                                }, 
                                {
                                    "field" : {
                                        "labels" : {
                                            "value" : [
                                                {
                                                    "literal" : "All"
                                                }, 
                                                {
                                                    "literal" : "Yo"
                                                }, 
                                                {
                                                    "literal" : "Yo1"
                                                }
                                            ], 
                                            "type" : "lit"
                                        }, 
                                        "selection" : {
                                            "value" : {
                                                "literal" : "All"
                                            }, 
                                            "type" : "lit"
                                        }, 
                                        "type" : "dropdown"
                                    },
                                    "required" : False,
                                    "label" : "DUState",
                                    "type" : "field"
                                }
                            ], 
                            "type" : "para"
                        }
                    ], 
                    "doc" : "slamdown"
                }
            }, 
            "cardType" : "markdown"
        }, 
        "556f65e7-7ef3-452f-9200-b3002611f799" : {
            "model" : {
                "ranges" : [

                ], 
                "text" : "# **Report for Deployment History of DUPackage**\r\n\r\n### Please select a DUPackage :\r\n\r\nDUPackage = {!`` select name from `/DPM/DeploymentManager/DeploymentUnitSet` order by name ``}"
            }, 
            "cardType" : "ace-markdown"
        }, 
        "5c92f8b6-c9cf-4fbd-92d4-4eed8ef0e3a2" : {
            "model" : {
                "ranges" : [

                ], 
                "text" : "### Please select a DUPackageState :\r\n\r\nState =    {!`` select s.name from `/DPM/DeploymentManager/State` as s join `/DPM/DeploymentManager/DeploymentUnitSet`as du \r\non oid(s.parent_entity_id)= du._id and \r\ndu.name =:DUPackage\r\norder by s.name ``}(All)"
            }, 
            "cardType" : "ace-markdown"
        }, 
        "6c71a330-ca9c-42d9-9200-fcc208bad7cf" : {
            "model" : {
                "ranges" : [

                ], 
                "text" : "### Please select a MachineGroup :\r\n\r\nMachineGroup = {!`` select group_name from `/DPM/DeploymentManager/MachineGroups` order by machine_name ``}"
            }, 
            "cardType" : "ace-markdown"
        }, 
        "a8b45a27-7f78-46c3-98e4-34f59b556073" : {
            "model" : {
                "pageSize" : None,
                "page" : None
            },
            "cardType" : "table"
        }, 
        "b5b11402-31a7-43a7-96e9-b879999cccaa" : {
            "model" : {
                "state" : {
                    "MachineGroup" : {
                        "labels" : {
                            "value" : [
                                {
                                    "literal" : "Test Dep"
                                }, 
                                {
                                    "literal" : "mm"
                                }, 
                                {
                                    "literal" : "Mast Wala Group"
                                }, 
                                {
                                    "literal" : "my group"
                                }, 
                                {
                                    "literal" : "sfd"
                                }
                            ], 
                            "type" : "lit"
                        }, 
                        "selection" : {
                            "value" : {
                                "literal" : "Mast Wala Group"
                            }, 
                            "type" : "lit"
                        }, 
                        "type" : "dropdown"
                    }
                }, 
                "input" : {
                    "blocks" : [
                        {
                            "content" : [
                                {
                                    "value" : "Please", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "select", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "a", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : "MachineGroup", 
                                    "type" : "str"
                                }, 
                                {
                                    "type" : "space"
                                }, 
                                {
                                    "value" : ":", 
                                    "type" : "str"
                                }
                            ],
                            "level" : 3,
                            "type" : "header"
                        }, 
                        {
                            "content" : [
                                {
                                    "type" : "softbreak"
                                }, 
                                {
                                    "field" : {
                                        "labels" : {
                                            "value" : [
                                                {
                                                    "literal" : "Test Dep"
                                                }, 
                                                {
                                                    "literal" : "mm"
                                                }, 
                                                {
                                                    "literal" : "Mast Wala Group"
                                                }, 
                                                {
                                                    "literal" : "my group"
                                                }, 
                                                {
                                                    "literal" : "sfd"
                                                }
                                            ], 
                                            "type" : "lit"
                                        },
                                        "selection" : None,
                                        "type" : "dropdown"
                                    },
                                    "required" : False,
                                    "label" : "MachineGroup",
                                    "type" : "field"
                                }
                            ], 
                            "type" : "para"
                        }
                    ], 
                    "doc" : "slamdown"
                }
            }, 
            "cardType" : "markdown"
        }, 
        "dcdfa4e9-5366-40aa-a3ec-054e7285e71b" : {
            "model" : {
                "layout" : {
                    "panes" : [
                        {
                            "pane" : {
                                "panes" : [
                                    {
                                        "pane" : {
                                            "panes" : [
                                                {
                                                    "pane" : {
                                                        "value" : "347ea5b9-1531-46b0-a029-69c0616c179e", 
                                                        "type" : "cell"
                                                    },
                                                    "ratio" : [ 
                                                        1, 
                                                        1
                                                    ]
                                                }
                                            ], 
                                            "orientation" : "vertical", 
                                            "type" : "split"
                                        },
                                        "ratio" : [ 
                                            1, 
                                            2
                                        ]
                                    }, 
                                    {
                                        "pane" : {
                                            "panes" : [
                                                {
                                                    "pane" : {
                                                        "value" : "ccacf276-02d3-4b01-b5c8-9600c56c5eee", 
                                                        "type" : "cell"
                                                    },
                                                    "ratio" : [ 
                                                        1, 
                                                        1
                                                    ]
                                                }
                                            ], 
                                            "orientation" : "vertical", 
                                            "type" : "split"
                                        },
                                        "ratio" : [ 
                                            1, 
                                            2
                                        ]
                                    }
                                ], 
                                "orientation" : "horizontal", 
                                "type" : "split"
                            },
                            "ratio" : [ 
                                2, 
                                7
                            ]
                        }, 
                        {
                            "pane" : {
                                "panes" : [
                                    {
                                        "pane" : {
                                            "panes" : [
                                                {
                                                    "pane" : {
                                                        "value" : "ac5966a2-4377-4ff2-8170-3b96a127c435", 
                                                        "type" : "cell"
                                                    },
                                                    "ratio" : [ 
                                                        1, 
                                                        1
                                                    ]
                                                }
                                            ], 
                                            "orientation" : "vertical", 
                                            "type" : "split"
                                        },
                                        "ratio" : [ 
                                            1, 
                                            2
                                        ]
                                    }, 
                                    {
                                        "pane" : {
                                            "panes" : [
                                                {
                                                    "pane" : {
                                                        "value" : "b1852407-91bb-425d-a826-c2c670500c84", 
                                                        "type" : "cell"
                                                    },
                                                    "ratio" : [ 
                                                        1, 
                                                        1
                                                    ]
                                                }
                                            ], 
                                            "orientation" : "vertical", 
                                            "type" : "split"
                                        },
                                        "ratio" : [ 
                                            1, 
                                            2
                                        ]
                                    }
                                ], 
                                "orientation" : "horizontal", 
                                "type" : "split"
                            },
                            "ratio" : [ 
                                25, 
                                84
                            ]
                        }, 
                        {
                            "pane" : {
                                "panes" : [
                                    {
                                        "pane" : {
                                            "value" : "8c0add71-fec4-4153-b96a-5dd0480c6f2e", 
                                            "type" : "cell"
                                        },
                                        "ratio" : [ 
                                            1, 
                                            1
                                        ]
                                    }
                                ], 
                                "orientation" : "horizontal", 
                                "type" : "split"
                            },
                            "ratio" : [ 
                                5, 
                                12
                            ]
                        }
                    ], 
                    "orientation" : "vertical", 
                    "type" : "split"
                }
            }, 
            "cardType" : "draftboard"
        }
    },
    "rootId" : "f8306699-668e-414a-b3ca-78986afd7c58",
    "version" : 2
}

]
