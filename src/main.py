from datetime import datetime
import flet as ft
from accountant.project import Project
from accountant.contract import Contract, Person, Room

from typing import Callable


class NewContractDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page, initial_project: Project, on_update: Callable):
        super().__init__(
            modal=True,
            title=ft.Text("新規契約の追加"),
            actions=[
                ft.TextButton("キャンセル", on_click=lambda e: page.close(self)),
                ft.TextButton(
                    "追加",
                    on_click=lambda e: self.submit_contract(
                        page, initial_project, on_update
                    ),
                ),
            ],
        )

        self.initialize_input_fields()

    def submit_contract(
        self, page: ft.Page, initial_project: Project, on_update: Callable
    ):
        new_contract = Contract(
            id=len(initial_project.contracts) + 1,
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
        initial_project.add_contract(new_contract)
        on_update()
        page.close(self)
        page.update()

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


def main(page: ft.Page):

    def open_contract(contract: Contract):
        # 契約の詳細をダイアログで表示
        details = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"契約詳細 (ID: {contract.id})"),
            content=ft.Column(
                [
                    ft.Text(f"Lessee: {contract.lessee.full_name}"),
                    ft.Text(f"Room: {contract.room.number}"),
                    ft.Text(f"Fee: {contract.fee}"),
                    ft.Text(f"Deposit: {contract.deposit}"),
                    ft.Text(f"Key Money: {contract.key_money}"),
                    ft.Text(f"Start: {contract.start}"),
                    ft.Text(f"End: {contract.end}"),
                    ft.Text(f"Transactions: {contract.transactions}"),
                ]
            ),
            actions=[ft.TextButton("閉じる", on_click=lambda e: page.close(details))],
        )
        page.open(details)
        page.update()

    def contract_texts(project: Project):
        if project.contracts:
            return [
                ft.ExpansionTile(
                    title=ft.Text(f"Contract {i+1}"),
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
                                    on_click=lambda e: open_contract(contract),
                                    icon=ft.Icons.EDIT,
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                )
                for i, contract in enumerate(project.contracts)
            ]
        else:
            return [ft.ExpansionTile(title=ft.Text("No contracts available"))]

    initial_project = Project("Initial Project")
    contract_display = ft.Column(
        contract_texts(initial_project),
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )

    def add_clicked(e):
        page.open(
            NewContractDialog(
                page,
                initial_project,
                update_contract_display,
            )
        )
        page.update()

    add_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_clicked)
    contract_display.controls.append(add_button)

    def update_contract_display():
        contract_display.controls = contract_texts(initial_project)
        contract_display.controls.append(add_button)
        contract_display.update()

    page.add(
        ft.SafeArea(
            ft.Container(
                contract_display,
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )


ft.app(main)
