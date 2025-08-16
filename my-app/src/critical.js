// !cc CRITICAL: Do not change logic without explicit approval
export function criticalLogic(input) {
	if (input == null) throw new Error('input required');
	return String(input).trim().toLowerCase();
}