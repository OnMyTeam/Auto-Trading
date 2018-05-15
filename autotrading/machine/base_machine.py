from abc import ABC,abstractmethod


class Machine(ABC):
    # @abstractmethod
    # def get_filled_orders(self):
    #     """
    #     체결정보 구하는 메소드
    #
    #     """
    #     pass
    @abstractmethod
    def get_ticker(self):
        """
        마지막 체결정보(Tick)를 구하는 메서드

        """
        pass
    # @abstractmethod
    # def get_wallet_status(self):
    #     """
    #     사용자 지갑정보 조회 메서드
    #
    #     """
    #     pass
    # @abstractmethod
    # def get_token(self):
    #     pass
    #
    # @abstractmethod
    # def set_token(self):
    #     pass
    #
    # @abstractmethod
    # def get_username(self):
    #
    #     pass
    #
    # @abstractmethod
    # def buy_order(self):
    #     """
    #     ㅐ무수주문 실행 메서드
    #
    #     """
    #     pass
    # @abstractmethod
    # def sell_order(self):
    #     """
    #     매도주문 실행 메서드
    #
    #     """
    #     pass
    #
    # @abstractmethod
    # def cancel_order(self):
    #     pass
    #
    # @abstractmethod
    # def get_my_order_status(self):
    #     pass

