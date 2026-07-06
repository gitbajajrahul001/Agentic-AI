
from app.models.vm_optimization_report import (
    VMOptimizationReport,
)
from dataclasses import asdict


class KnowledgeSerializer:
    """
    Converts a VM optimization report into
    a canonical knowledge document.
    """

    ####################################################################
    # Public API
    ####################################################################
        
    def serialize(
        self,
        report: VMOptimizationReport,
    ) -> dict:

        return {

            "execution": self._serialize_execution(
                report,
            ),

            "inventory": self._serialize_inventory(
                report,
            ),

            "metadata": self._serialize_metadata(
                report,
            ),

            "observability": self._serialize_observability(
                report,
            ),
            "analysis": self._serialize_analysis(
                report,
            ),
        }

    ####################################################################
    # Serialization
    ####################################################################

    def _serialize_execution(
        self,
        report: VMOptimizationReport,
    ) -> dict:

        return {

            "execution_id": (
                report.execution_id
                ),
            
            "generated_at": (
                report.generated_at.isoformat()
            ),

            "policy_version": (
                report.policy_version
            ),
        }

    def _serialize_inventory(
        self,
        report: VMOptimizationReport,
    ) -> dict:

        vm = report.virtual_machine

        return {

            "resource_id": (
                vm.id
            ),

            "resource_name": (
                vm.name
            ),

            "resource_type": (
                "Microsoft.Compute/virtualMachines"
            ),

            "subscription_id": (
                vm.subscription_id
            ),

            "resource_group": (
                vm.resource_group
            ),

            "location": (
                vm.location
            ),

            "current_sku": (
                vm.vm_size
            ),

            "operating_system": (
                vm.operating_system
            ),

            "power_state": (
                vm.power_state
            ),
        }

    def _serialize_metadata(
        self,
        report: VMOptimizationReport,
    ) -> dict:

        metadata = {}

        for key, value in report.metadata.items():

            if value:

                metadata[key] = value

        return metadata

    def _serialize_observability(
        self,
        report: VMOptimizationReport,
    ) -> dict:

        metrics = report.metrics

        return {

            "sample_count": (
                metrics.sample_count
            ),

            "cpu_average_percent": (
                metrics.cpu_average_percent
            ),

            "memory_average_percent": (
                metrics.memory_average_percent
            ),
        }

    def _serialize_analysis(
        self,
        report: VMOptimizationReport,
    ) -> dict:

        return {

            "recommendation": (
                self._serialize_recommendation(
                    report,
                )
            ),

            "validation": (
                self._serialize_validation(
                    report,
                )
            ),

            "cost": (
                self._serialize_cost(
                    report,
                )
            ),
        }


    def _serialize_recommendation(
        self,
        report: VMOptimizationReport,
    ) -> dict:

        analysis = report.analysis

        return {

            "pre_validation": (
                self._display_name(
                    analysis.recommendation.value
                    )
            ),

            "post_validation": (
                    self._display_name(
                        analysis.final_recommendation.value
                    )
            ),
            "confidence": (
                    self._display_name(
                        analysis.confidence.value
                    )
            ),

            "recommended_sku": (
                analysis.recommended_vm_size
            ),

            "reasons": [

                {

                    "category": (
                        reason.category
                    ),

                    "message": (
                        reason.message
                    ),
                }

                for reason in analysis.reasons
            ],
        }


    def _serialize_validation(
        self,
        report: VMOptimizationReport,
    ) -> dict:

        analysis = report.analysis

        return {

            "passed": all(

                evaluation.passed_validation

                for evaluation in (
                    analysis.candidate_evaluations
                )
            ),

            "candidate_evaluations": [

                {

                    "candidate_sku": (
                        evaluation.candidate_vm_size
                    ),

                    "passed": (
                        evaluation.passed_validation
                    ),

                    "summary": (
                        asdict(
                            evaluation.validation_summary
                        )
                    ),
                }

                for evaluation in (
                    analysis.candidate_evaluations
                )
            ],
        }



    def _serialize_cost(
        self,
        report: VMOptimizationReport,
    ) -> dict:

        cost = report.cost_analysis

        return {

            "currency": (
                cost.currency
            ),

            "current_hourly_cost": (
                cost.current_hourly_cost
            ),

            "recommended_hourly_cost": (
                cost.recommended_hourly_cost
            ),

            "current_monthly_cost": (
                cost.current_monthly_cost
            ),

            "recommended_monthly_cost": (
                cost.recommended_monthly_cost
            ),

            "monthly_savings": (
                cost.monthly_savings
            ),

            "annual_savings": (
                cost.yearly_savings
            ),
        }

    def _display_name(
        self,
        value: str,
    ) -> str:

        return (

            value

            .replace(
                "_",
                " ",
            )

            .title()
        )