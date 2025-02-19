from ..core.agent import Agent
from ..core.tasks import Task

class ManufacturingAgent(Agent):
    """Agent responsible for manufacturing process optimization, supply chain management, and quality control."""

    def __init__(self):
        super().__init__()
        self.name = "Manufacturing Agent"

    def optimize_process(self, process_data):
        """Analyze and optimize manufacturing processes."""
        analysis = self._analyze_process_data(process_data)
        return self._generate_optimization_recommendations(analysis)

    def manage_supply_chain(self, supply_chain_data):
        """Monitor and optimize supply chain operations."""
        status = self._analyze_supply_chain(supply_chain_data)
        return {
            'inventory_levels': self._check_inventory_levels(status),
            'supplier_performance': self._evaluate_supplier_performance(status),
            'optimization_suggestions': self._generate_supply_chain_recommendations(status)
        }

    def control_quality(self, production_data):
        """Ensure product quality through continuous monitoring and analysis."""
        quality_metrics = self._analyze_quality_metrics(production_data)
        if self._detect_quality_issues(quality_metrics):
            self._trigger_quality_alert(quality_metrics)
        return self._generate_quality_report(quality_metrics)

    def _analyze_process_data(self, data):
        """Analyze manufacturing process data."""
        return {
            'efficiency': self._calculate_process_efficiency(data),
            'bottlenecks': self._identify_bottlenecks(data),
            'resource_utilization': self._analyze_resource_usage(data),
            'cycle_time': self._calculate_cycle_time(data)
        }

    def _calculate_process_efficiency(self, data):
        """Calculate overall process efficiency."""
        production_time = data.get('production_time', 0)
        planned_time = data.get('planned_time', 1)  # Avoid division by zero
        return (production_time / planned_time) * 100 if planned_time > 0 else 0

    def _identify_bottlenecks(self, data):
        """Identify process bottlenecks."""
        bottlenecks = []
        process_steps = data.get('process_steps', {})
        for step, metrics in process_steps.items():
            if metrics.get('utilization', 0) > 90:
                bottlenecks.append({
                    'step': step,
                    'utilization': metrics.get('utilization'),
                    'impact': metrics.get('downstream_delay', 0)
                })
        return bottlenecks

    def _analyze_resource_usage(self, data):
        """Analyze resource utilization."""
        return {
            'labor': data.get('labor_utilization', 0),
            'equipment': data.get('equipment_utilization', 0),
            'materials': data.get('material_efficiency', 0)
        }

    def _calculate_cycle_time(self, data):
        """Calculate manufacturing cycle time."""
        return {
            'total_time': data.get('total_cycle_time', 0),
            'processing_time': data.get('processing_time', 0),
            'wait_time': data.get('wait_time', 0),
            'transport_time': data.get('transport_time', 0)
        }

    def _analyze_supply_chain(self, data):
        """Analyze supply chain operations and performance."""
        return {
            'inventory': self._analyze_inventory_data(data.get('inventory', {})),
            'suppliers': self._analyze_supplier_data(data.get('suppliers', {})),
            'logistics': self._analyze_logistics_data(data.get('logistics', {}))
        }

    def _analyze_inventory_data(self, inventory_data):
        """Analyze inventory metrics."""
        return {
            'stock_levels': inventory_data.get('current_stock', {}),
            'turnover_rate': inventory_data.get('turnover_rate', 0),
            'holding_cost': inventory_data.get('holding_cost', 0)
        }

    def _analyze_supplier_data(self, supplier_data):
        """Analyze supplier performance metrics."""
        return {
            'delivery_time': supplier_data.get('avg_delivery_time', 0),
            'quality_rating': supplier_data.get('quality_rating', 0),
            'cost_efficiency': supplier_data.get('cost_efficiency', 0)
        }

    def _analyze_logistics_data(self, logistics_data):
        """Analyze logistics performance."""
        return {
            'shipping_time': logistics_data.get('avg_shipping_time', 0),
            'shipping_cost': logistics_data.get('shipping_cost', 0),
            'delivery_accuracy': logistics_data.get('delivery_accuracy', 0)
        }

    def _analyze_quality_metrics(self, data):
        """Analyze product quality metrics."""
        return {
            'defect_rate': self._calculate_defect_rate(data),
            'quality_scores': self._calculate_quality_scores(data),
            'compliance': self._check_compliance(data)
        }

    def _calculate_defect_rate(self, data):
        """Calculate product defect rate."""
        total_units = data.get('total_units', 0)
        defective_units = data.get('defective_units', 0)
        return (defective_units / total_units * 100) if total_units > 0 else 0

    def _calculate_quality_scores(self, data):
        """Calculate quality scores for different metrics."""
        return {
            'dimensional_accuracy': data.get('dimensional_accuracy', 0),
            'surface_finish': data.get('surface_finish', 0),
            'functional_tests': data.get('functional_tests', 0)
        }

    def _check_compliance(self, data):
        """Check compliance with quality standards."""
        return {
            'standards_met': data.get('standards_met', []),
            'violations': data.get('violations', []),
            'certification_status': data.get('certification_status', 'unknown')
        }

    def _detect_quality_issues(self, metrics):
        """Detect potential quality issues."""
        issues = []
        if metrics['defect_rate'] > 5:  # 5% threshold
            issues.append({
                'type': 'high_defect_rate',
                'value': metrics['defect_rate'],
                'threshold': 5
            })
        for metric, score in metrics['quality_scores'].items():
            if score < 80:  # 80% quality threshold
                issues.append({
                    'type': f'low_{metric}_score',
                    'value': score,
                    'threshold': 80
                })
        return issues

    def _trigger_quality_alert(self, metrics):
        """Trigger alerts for quality issues."""
        issues = self._detect_quality_issues(metrics)
        if issues:
            return {
                'alert_level': 'high' if any(i['type'] == 'high_defect_rate' for i in issues) else 'medium',
                'issues': issues,
                'timestamp': metrics.get('timestamp', None)
            }
        return None

    def _generate_quality_report(self, metrics):
        """Generate comprehensive quality report."""
        return {
            'summary': {
                'overall_quality_score': sum(metrics['quality_scores'].values()) / len(metrics['quality_scores']),
                'defect_rate': metrics['defect_rate'],
                'compliance_status': metrics['compliance']['certification_status']
            },
            'detailed_metrics': metrics['quality_scores'],
            'compliance_details': metrics['compliance'],
            'issues': self._detect_quality_issues(metrics),
            'recommendations': self._generate_quality_recommendations(metrics)
        }