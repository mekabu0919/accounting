import flet as ft
from accountant.project import Project
from accountant.contract import Contract, Person


def contract_texts(project: Project):
    if project.contracts:
        return [
            ft.ExpansionTile(
                title=ft.Text(f"Contract {i+1}"),
                subtitle=ft.Text(f"Lessee: {contract.lessee.full_name}, Room: {contract.room}"),
                leading=ft.Icon(ft.Icons.HOUSE),
                controls=[
                    ft.Text(f"Fee: {contract.fee}"),
                    ft.Text(f"Deposit: {contract.deposit}"),
                    ft.Text(f"Key Money: {contract.key_money}"),
                    ft.Text(f"Start: {contract.start}"),
                    ft.Text(f"End: {contract.end}"),
                    ft.Text(f"Transactions: {contract.transactions}"),
                ],
            )
            for i, contract in enumerate(project.contracts)
        ]
    else:
        return [ft.ExpansionTile(title=ft.Text("No contracts available"))]


def main(page: ft.Page):

    initial_project = Project("Initial Project")
    contract_display = ft.Column(
        contract_texts(initial_project),
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )

    def add_contract(e):
        new_contract = Contract.from_json(
            {
                "id": len(initial_project.contracts) + 1,
                "lessee": {"family_name": "New", "given_name": "Lessee"},
                "room": "New Room",
                "fee": 1000,
                "deposit": 2000,
                "key_money": 300,
                "start": "2023-01-01",
                "end": "2023-12-31",
                "transactions": [],
            }
        )
        initial_project.add_contract(new_contract)
        update_contract_display()

    add_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_contract)
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
