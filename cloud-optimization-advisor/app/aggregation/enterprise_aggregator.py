from app.models.enterprise_knowledge import (
    EnterpriseKnowledge,
)


class EnterpriseAggregator:

    def aggregate(
        self,
        subscription_documents: list[dict],
    ) -> EnterpriseKnowledge:

        
        ###################################################
        # Initialize Aggregation Variables
        ###################################################

        keep_current = 0
        downsize = 0
        upsize = 0

        subscription_count = len(
            subscription_documents
        )

        resource_group_count = 0

        vm_count = 0

        monthly_savings = 0.0
        annual_savings = 0.0

        source_documents = []
        
        ###################################################
        # Aggregate Subscription Knowledge
        ###################################################

        for subscription in subscription_documents:

            keep_current += (
                subscription["optimization"]["keep_current"]
            )

            downsize += (
                subscription["optimization"]["downsize"]
            )

            upsize += (
                subscription["optimization"]["upsize"]
            )

            resource_group_count += (
                subscription["inventory"]["resource_group_count"]
            )

            vm_count += (
                subscription["inventory"]["vm_count"]
            )

            monthly_savings += (
                subscription["financial"]["monthly_savings"]
            )

            annual_savings += (
                subscription["financial"]["annual_savings"]
            )

            source_documents.append(
                subscription["subscription"]["subscription_id"]
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
                "All virtual machines across the Azure estate are appropriately sized."
            )

        else:

            summary = (
                f"{downsize} virtual machine(s) across the Azure estate are candidates for downsizing."
            )
                
        ###################################################
        # Build Enterprise Knowledge
        ###################################################

        enterprise_document = EnterpriseKnowledge(

            execution=subscription_documents[0]["execution"],

            enterprise={

                "name": "Azure Estate",

            },

            inventory={

                "subscription_count": subscription_count,

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

        return enterprise_document