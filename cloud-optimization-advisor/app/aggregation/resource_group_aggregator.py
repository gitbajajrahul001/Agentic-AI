from collections import defaultdict
from pathlib import Path
import json

from app.models.resource_group_knowledge import (
    ResourceGroupKnowledge,
)



class ResourceGroupAggregator:

    def load_vm_documents(
        self,
        vm_document_files: list[str],
    ) -> list[dict]:

        vm_documents = []

        for file in vm_document_files:

            with open(
                file,
                "r",
                encoding="utf-8",
            ) as f:

                vm_documents.append(
                    json.load(f)
                )

        return vm_documents 
       


    def aggregate(
            self,
            vm_documents: list[dict],
        ) -> list[ResourceGroupKnowledge]:

            grouped_documents = defaultdict(list)

            for vm in vm_documents:

                grouped_documents[
                    vm["inventory"]["resource_group"]
                ].append(vm)

            resource_group_documents = []

            for resource_group, virtual_machines in grouped_documents.items():
                
                ###################################################
                # Initialize Aggregation Variables
                ###################################################
                

                keep_current = 0
                downsize = 0
                upsize = 0
                
                monthly_savings = 0.0
                annual_savings = 0.0

                source_documents = []
                
                ###################################################
                # Aggregate VM Knowledge
                ###################################################                         
               
               
                for vm in virtual_machines:

                    recommendation = (
                        vm["analysis"]["recommendation"]["post_validation"]
                    )

                    if recommendation == "Keep Current Size":
                        keep_current += 1

                    elif recommendation == "Downsize":
                        downsize += 1

                    elif recommendation == "Upsize":
                        upsize += 1

                    monthly_savings += (
                        vm["analysis"]["cost"]["monthly_savings"]
                    )

                    annual_savings += (
                        vm["analysis"]["cost"]["annual_savings"]
                    )

                    source_documents.append(
                        vm["inventory"]["resource_name"]
                    )   
                
                    
                ###################################################
                # Calculate Derived Metrics
                ###################################################

                total_vms = len(virtual_machines)

                optimization_score = 0.0

                if total_vms > 0:

                    optimization_score = round(
                        (keep_current / total_vms) * 100,
                        1,
                    )

                ###################################################
                # Generate Insights
                ###################################################

                if downsize == 0:

                    summary = (
                        "All virtual machines are appropriately sized."
                    )

                else:

                    summary = (
                        f"{downsize} virtual machine(s) are candidates for downsizing."
                    )
                execution = virtual_machines[0]["execution"]

                ###################################################
                # Build Resource Group Knowledge
                ###################################################

                rg_document = ResourceGroupKnowledge(

                    execution=execution,

                    resource_group={

                        "name": resource_group,

                        "subscription_id":
                            virtual_machines[0]["inventory"]["subscription_id"],

                        "location":
                            virtual_machines[0]["inventory"]["location"],
                    },

                    inventory={

                        "vm_count": len(virtual_machines),
                    },

                    optimization={

                        "keep_current": keep_current,

                        "downsize": downsize,

                        "upsize": upsize,

                        "optimization_score": optimization_score,
                    },

                    insights={

                        "summary": summary,
                    },

                    financial={

                        "monthly_savings": monthly_savings,

                        "annual_savings": annual_savings,
                    },

                    source_documents=source_documents,
                )

                resource_group_documents.append(
                    rg_document
                )

            return resource_group_documents