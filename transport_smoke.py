from hyperxi_lab_viewer.transport import Flag, apply_word, orbit_length, summary


def main() -> None:
    seed = Flag(face=0, slot=0, orient=0)

    print("TRANSPORT SMOKE TEST")
    print("====================")
    print(f"seed: {seed}")
    print(f"S   -> {apply_word(seed, 'S')}")
    print(f"F   -> {apply_word(seed, 'F')}")
    print(f"V   -> {apply_word(seed, 'V')}")
    print(f"FSF -> {apply_word(seed, 'FSF')}")
    print()

    for line in summary("FSF"):
        print(line)
    print(f"orbit length from seed under FSF: {orbit_length(seed, 'FSF')}")


if __name__ == "__main__":
    main()
