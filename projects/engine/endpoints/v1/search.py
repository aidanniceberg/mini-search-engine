from flask import Blueprint, g, jsonify, request

from src.services import RewardService


class RewardsAPI(Blueprint):
    def __init__(self):
        super().__init__("rewards", __name__)
        self.reward_service = RewardService()

        self.add_url_rule("/", methods=["GET"], view_func=self.get_rewards)
        self.add_url_rule("/total", methods=["GET"], view_func=self.get_total)

    def get_rewards(self):
        # TODO: change to real authentication
        user_id = request.args.get("user", type=int)
        page = request.args.get("page", 1, type=int)
        size = request.args.get("size", 10, type=int)
        reward_type = request.args.get("type", None)
        if user_id is None:
            return "user_id is missing", 400
        if reward_type not in {"direct", "indirect", None}:
            return "Invalid reward type", 400
        direct = reward_type in {"direct", None}
        indirect = reward_type in {"indirect", None}
        rewards = self.reward_service.get_rewards_by_user(
            user_id=user_id,
            page=page,
            page_size=size,
            direct=direct,
            indirect=indirect,
        )
        rewards_dict = {
            key: [reward.as_dict() for reward in rewards]
            for key, rewards in rewards.items()
            if rewards is not None
        }
        return jsonify(rewards_dict)

    def get_total(self):
        user_id = request.args.get("user", type=int)
        if user_id is None:
            raise RuntimeError("user_id is missing")
        result = self.reward_service.get_total_credits(user_id=user_id)
        return jsonify(result)
