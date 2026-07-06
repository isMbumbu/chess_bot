from dataclasses import dataclass

import chess
from playwright.async_api import Locator, Page


@dataclass(frozen=True)
class BoardSelectors:
    board: str = "[data-testid='board']"
    square: str = "[data-square]"
    piece: str = "[data-piece]"
    fen: str | None = "[data-fen]"


@dataclass(frozen=True)
class ParsedPiece:
    square: str
    piece: str


async def board_from_dom(page: Page, selectors: BoardSelectors) -> chess.Board:
    fen = await fen_from_dom(page, selectors)
    if fen is not None:
        return chess.Board(fen)

    pieces = await pieces_from_dom(page.locator(selectors.board), selectors)
    board = chess.Board.empty()

    for parsed_piece in pieces:
        square = chess.parse_square(parsed_piece.square)
        piece = chess.Piece.from_symbol(parsed_piece.piece)
        board.set_piece_at(square, piece)

    board.turn = await active_color_from_dom(page)
    board.castling_rights = chess.BB_EMPTY
    board.ep_square = None
    return board


async def fen_from_dom(page: Page, selectors: BoardSelectors) -> str | None:
    if selectors.fen is None:
        return None

    locator = page.locator(selectors.fen).first
    if await locator.count() == 0:
        return None

    fen = await locator.get_attribute("data-fen")
    return fen or None


async def pieces_from_dom(
    board_locator: Locator,
    selectors: BoardSelectors,
) -> list[ParsedPiece]:
    squares = board_locator.locator(selectors.square)
    parsed: list[ParsedPiece] = []

    for index in range(await squares.count()):
        square = squares.nth(index)
        square_name = await square.get_attribute("data-square")
        piece = square.locator(selectors.piece).first

        if await piece.count() == 0:
            continue

        piece_symbol = await piece.get_attribute("data-piece")

        if square_name is None or piece_symbol is None:
            continue

        parsed.append(ParsedPiece(square=square_name, piece=piece_symbol))

    return parsed


async def active_color_from_dom(page: Page) -> bool:
    turn_locator = page.locator("[data-turn]").first
    if await turn_locator.count() == 0:
        return chess.WHITE

    turn = await turn_locator.get_attribute("data-turn")
    return chess.WHITE if turn != "black" else chess.BLACK
