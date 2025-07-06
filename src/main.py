from datetime import datetime
import flet as ft
from accountant.project import Project
from accountant.contract import Contract, Person, Room

from typing import Callable


class NewContractDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page, id: int, on_dismiss: Callable):
        super().__init__(
            modal=True,
            title=ft.Text("新規契約の追加"),
            actions=[
                ft.TextButton("キャンセル", on_click=lambda e: page.close(self)),
                ft.TextButton(
                    "追加",
                    on_click=lambda e: self.submit_contract(),
                ),
            ],
            on_dismiss=on_dismiss,
        )
        self.page: ft.Page = page
        self.id = id
        self.result = None
        self.initialize_input_fields()

    def submit_contract(self):
        new_contract = Contract(
            id=self.id,
            lessee=Person(
                family_name=self.lessee_family.value,
                given_name=self.lessee_given.value,
            ),
            room=Room(
                id=1,
                number=self.room_number.value,
            ),
            fee=int(self.fee.value),
            deposit=int(self.deposit.value),
            key_money=int(self.key_money.value),
            start=datetime.strptime(self.start.value, "%Y-%m-%d").date(),
            end=datetime.strptime(self.end.value, "%Y-%m-%d").date(),
        )
        self.result = new_contract
        self.page.close(self)

    def initialize_input_fields(self):
        self.lessee_family = ft.TextField(label="Lessee Family Name", value="Smith")
        self.lessee_given = ft.TextField(label="Lessee Given Name", value="John")
        self.room_number = ft.TextField(label="Room Number", value="101")
        self.fee = ft.TextField(label="Fee", value="1000")
        self.deposit = ft.TextField(label="Deposit", value="2000")
        self.key_money = ft.TextField(label="Key Money", value="300")
        self.start = ft.TextField(label="Start", value="2023-01-01")
        self.end = ft.TextField(label="End", value="2023-12-31")

        self.content = ft.Column(
            [
                self.lessee_family,
                self.lessee_given,
                self.room_number,
                self.fee,
                self.deposit,
                self.key_money,
                self.start,
                self.end,
            ]
        )


class ContractDisplayTile(ft.ExpansionTile):
    def __init__(self, contract: Contract, page: ft.Page):
        super().__init__(
            title=ft.Text(f"Contract {contract.id}"),
            subtitle=ft.Text(
                f"Lessee: {contract.lessee.full_name}, Room: {contract.room.number}"
            ),
            leading=ft.Icon(ft.Icons.HOUSE),
            controls=[
                ft.Text(f"Fee: {contract.fee}"),
                ft.Text(f"Deposit: {contract.deposit}"),
                ft.Text(f"Key Money: {contract.key_money}"),
                ft.Text(f"Start: {contract.start}"),
                ft.Text(f"End: {contract.end}"),
                ft.Text(f"Transactions: {contract.transactions}"),
                ft.Row(
                    [
                        ft.TextButton(
                            "Open",
                            on_click=lambda e: self.open_contract(),
                            icon=ft.Icons.EDIT,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
        )
        self.contract = contract
        self.page: ft.Page = page

    def open_contract(self):
        # 契約の詳細をダイアログで表示
        details = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"契約詳細 (ID: {self.contract.id})"),
            content=ft.Column(
                [
                    ft.Text(f"Lessee: {self.contract.lessee.full_name}"),
                    ft.Text(f"Room: {self.contract.room.number}"),
                    ft.Text(f"Fee: {self.contract.fee}"),
                    ft.Text(f"Deposit: {self.contract.deposit}"),
                    ft.Text(f"Key Money: {self.contract.key_money}"),
                    ft.Text(f"Start: {self.contract.start}"),
                    ft.Text(f"End: {self.contract.end}"),
                    ft.Text(f"Transactions: {self.contract.transactions}"),
                ]
            ),
            actions=[ft.TextButton("閉じる", on_click=lambda e: self.page.close(details))],
        )
        self.page.open(details)


def create_contract_texts(project: Project, page: ft.Page):
    if project.contracts:
        return [
            ContractDisplayTile(contract, page)
            for contract in project.contracts
        ]
    else:
        return [ft.ExpansionTile(title=ft.Text("No contracts available"))]


class ContractDisplay(ft.Column):
    def __init__(self, project: Project, page: ft.Page):
        super().__init__(
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
        self.project = project
        self.page: ft.Page = page
        self.add_button = ft.IconButton(
            icon=ft.Icons.ADD, on_click=self.add_button_clicked
        )
        self.controls = create_contract_texts(self.project, self.page)
        self.controls.append(self.add_button)

    def add_button_clicked(self, e):
        self.page.open(
            NewContractDialog(
                self.page,
                len(self.project.contracts) + 1,
                self.show_contracts,
            )
        )
        self.page.update()

    def show_contracts(self, e: ft.ControlEvent):
        if e.control.result is not None:
            self.project.add_contract(e.control.result)
        self.controls = create_contract_texts(self.project, self.page)
        self.controls.append(self.add_button)
        self.update()


class App(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(alignment=ft.MainAxisAlignment.CENTER, expand=True)
        self.page = page
        self.project = Project("My Project")
        self.contract_display = ContractDisplay(self.project, page)
        self.controls.append(self.contract_display)


def main(page: ft.Page):
    page.title = "Accounting App"
    page.add(
        ft.SafeArea(
            ft.Container(
                App(page),
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )


ft.app(main)
