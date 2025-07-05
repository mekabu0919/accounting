from datetime import datetime
import flet as ft
from accountant.project import Project
from accountant.contract import Contract, Person, Room


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

    # 入力用ダイアログの定義
    lessee_family = ft.TextField(label="Lessee Family Name")
    lessee_given = ft.TextField(label="Lessee Given Name")
    room_number = ft.TextField(label="Room Number")
    fee = ft.TextField(label="Fee", value="1000")
    deposit = ft.TextField(label="Deposit", value="2000")
    key_money = ft.TextField(label="Key Money", value="300")
    start = ft.TextField(label="Start", value="2023-01-01")
    end = ft.TextField(label="End", value="2023-12-31")

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("新規契約の追加"),
        content=ft.Column(
            [
                lessee_family,
                lessee_given,
                room_number,
                fee,
                deposit,
                key_money,
                start,
                end,
            ]
        ),
        actions=[
            ft.TextButton("キャンセル", on_click=lambda e: page.close(dialog)),
            ft.TextButton("追加", on_click=lambda e: submit_contract()),
        ],
    )

    def submit_contract():
        new_contract = Contract(
            id=len(initial_project.contracts) + 1,
            lessee=Person(
                family_name=lessee_family.value,
                given_name=lessee_given.value,
            ),
            room=Room(
                id=1,
                number=room_number.value,
            ),
            fee=int(fee.value),
            deposit=int(deposit.value),
            key_money=int(key_money.value),
            start=datetime.strptime(start.value, "%Y-%m-%d").date(),
            end=datetime.strptime(end.value, "%Y-%m-%d").date(),
        )
        initial_project.add_contract(new_contract)
        update_contract_display()
        page.close(dialog)
        page.update()

    def add_contract(e):
        # 入力欄を初期化
        lessee_family.value = ""
        lessee_given.value = ""
        room_number.value = ""
        fee.value = "1000"
        deposit.value = "2000"
        key_money.value = "300"
        start.value = "2023-01-01"
        end.value = "2023-12-31"
        page.open(dialog)
        page.update()

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
