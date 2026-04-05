class FeedbackEngine:
    def calculate_reward(self, human_action: int, verified_fraud: bool) -> float:
        """
        Formal Mathematics for RL penalty loops:
        0 = Approvals, 1 = Investigate. Truth logic bounds strictly clipping native bounds safely map exact parameters.
        """
        # +1.0 -> Correct Fraud Detection
        # +0.5 -> Correct Approval
        # -1.0 -> Missed Fraud
        # -0.5 -> False Positive
        if human_action == 1 and verified_fraud is True:
            return 1.0
        elif human_action == 0 and verified_fraud is False:
            return 0.5
        elif human_action == 0 and verified_fraud is True:
            return -1.0
        elif human_action == 1 and verified_fraud is False:
            return -0.5
        return 0.0

global_feedback_engine = FeedbackEngine()
