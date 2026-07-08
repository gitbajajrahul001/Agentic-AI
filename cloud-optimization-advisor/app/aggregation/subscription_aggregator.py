from collections import defaultdict

from app.models.subscription_knowledge import (
    SubscriptionKnowledge,
)


class SubscriptionAggregator:

    def aggregate(
        self,
        resource_group_documents: list[dict],
    ) -> list[SubscriptionKnowledge]:

        grouped_documents = defaultdict(list)

        for resource_group in resource_group_documents:

            grouped_documents[
                resource_group["resource_group"]["subscription_id"]
            ].append(resource_group)
            
        subscription_documents = []
        
        ###################################################
        # Aggregate Resource Group Knowledge
        ###################################################
        
        for subscription_id, resource_groups in grouped_documents.items():

            ###################################################
            # Initialize Aggregation Variables
            ###################################################

            keep_current = 0
            downsize = 0
            upsize = 0

            monthly_savings = 0.0
            annual_savings = 0.0

            resource_group_count = len(
                resource_groups
            )

            vm_count = 0

            source_documents = []
            
            
            for resource_group in resource_groups:

                keep_current += (
                    resource_group["optimization"]["keep_current"]
                )

                downsize += (
                    resource_group["optimization"]["downsize"]
                )

                upsize += (
                    resource_group["optimization"]["upsize"]
                )

                vm_count += (
                    resource_group["inventory"]["vm_count"]
                )

                monthly_savings += (
                    resource_group["financial"]["monthly_savings"]
                )

                annual_savings += (
                    resource_group["financial"]["annual_savings"]
                )

                source_documents.append(
                    resource_group["resource_group"]["name"]
                )
            
            ###################################################
            # Calculate Derived Metrics
            ###################################################

            optimization_score = round(

                (keep_current / vm_count) * 100,

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
                    ###################################################
        # Build Subscription Knowledge
        ###################################################

        subscription_document = SubscriptionKnowledge(

            execution=resource_groups[0]["execution"],

            subscription={

                "subscription_id": subscription_id,

            },

            inventory={

                "resource_group_count": resource_group_count,

                "vm_count": vm_count,

            },

            optimization={

                "keep_current": keep_current,

                "downsize": downsize,

                "upsize": upsize,

                "optimization_score": optimization_score,

            },

            financial={

                "monthly_savings": monthly_savings,

                "annual_savings": annual_savings,

            },

            insights={

                "summary": summary,

            },

            source_documents=source_documents,

        )

        subscription_documents.append(
            subscription_document
        )
        
        return subscription_documents
            