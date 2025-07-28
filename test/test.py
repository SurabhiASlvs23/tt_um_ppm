# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_ppm(dut):
    dut._log.info("Starting Pulse Position Modulator Test")

    # Set the clock to 10 us period (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Applying reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    # Example test: Send pulse at position 3 (i.e., ui_in = 3)
    test_position = 3
    dut.ui_in.value = test_position
    await ClockCycles(dut.clk, 1)

    expected = 1 << test_position
    dut._log.info(f"Expecting pulse at bit {test_position}, expected output: {expected:#010b}")
    assert dut.uo_out.value == expected, f"Expected {expected:#010b}, got {int(dut.uo_out.value):#010b}"

    # Try another position
    test_position = 6
    dut.ui_in.value = test_position
    await ClockCycles(dut.clk, 1)

    expected = 1 << test_position
    dut._log.info(f"Expecting pulse at bit {test_position}, expected output: {expected:#010b}")
    assert dut.uo_out.value == expected, f"Expected {expected:#010b}, got {int(dut.uo_out.value):#010b}"
