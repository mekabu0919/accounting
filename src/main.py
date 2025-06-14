import flet as ft
from accountant.project import Project
from accountant.contract import Contract


def main(page: ft.Page):
    initial_project = Project("Initial Project")
    contract_display = ft.Column(
        [
            ft.Text(
                f"Contracts: {initial_project.contracts[0].to_json() if initial_project.contracts else 'No contracts available'}"
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )

    def add_contract(e):
        new_contract = Contract.from_json(
            {
                "fee": 1000,
                "deposit": 2000,
                "key_money": 300,
                "start": "2023-01-01",
                "end": "2023-12-31",
                "transactions": [],
            }
        )
        initial_project.add_contract(new_contract)
        contract_display.controls.append(
            ft.Text(f"New Contract: {new_contract.to_json()}")
        )
        contract_display.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=add_contract
    )
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
