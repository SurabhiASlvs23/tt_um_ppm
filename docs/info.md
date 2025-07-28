<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->
## Credits
We gratefully acknowledge the Center of Excellence (CoE) in Integrated Circuits and Systems (ICAS) and the Department of Electronics and Communication Engineering (ECE) for providing the necessary resources and guidance.
Special thanks to Dr. K. S. Geetha (Vice Principal) and Dr. K. N. Subramanya (Principal) for their constant encouragement and support in facilitating this Tiny Tapeout 8 submission.

## How it works

The tt_um_ppm module implements an 8-bit Pulse Position Modulator (PPM), a scheme commonly used in wireless communications, servo control, and digital signaling. The PPM scheme modulates the position of a fixed-width pulse within a time window, depending on the input value.

In this design, the 8-bit input ui_in determines the position (time offset) of a single-cycle pulse within a 256-clock cycle frame. A counter runs from 0 to 255 continuously. When the counter value equals the ui_in input, the module asserts a 1-bit pulse on the output (uo_out[7]) for one clock cycle. All other bits of uo_out remain 0.

The design is clock-driven and synchronous, with an active-low asynchronous reset (rst_n) to initialize the internal state.
## Functional Description
# Input and Output Port
- **Inputs:**
  - `clk` – Clock signal (10 μs period or 100 KHz)
  - `rst_n` – Active-low synchronous reset
  - `ena` – Module enable
  - `ui_in[7:0]` – Dedicated 8-bit input (data input)
  - `uio_in[7:0]` – General-purpose IO input (unused)

- **Outputs:**
  - `uo_out[7:0]` – 8-bit output representing generated PPM signal
  - `uio_out[7:0]` – General-purpose IO output (unused)
  - `uio_oe[7:0]` – Output enable for `uio_out` (unused)

When `ena` is asserted and `rst_n` is deasserted, the module reads the input byte `ui_in` and encodes it into a single output pulse at a position (time slot) within the PPM frame. The output `uo_out` reflects this PPM behavior (only one bit is high at a time, the rest are low).

## Internal Architecture
# Counter Logic
A simple 8-bit counter increments on every rising edge of the clock. It wraps around from 255 back to 0. The counter continuously cycles, forming a timing window.

# Pulse Generation Logic
Whenever the internal counter equals the value of ui_in, a single-cycle pulse is asserted on uo_out[7]. This pulse represents the encoded position, and all other outputs are zero. The system resets cleanly on rst_n.

# Reset Behavior
When rst_n is deasserted (low):

The internal counter is reset to 0.

The pulse output is cleared.

The system returns to a known initial state.

# Unused Logic Handling
uio_in, ena, and other unused inputs are logically consumed using bitwise operations to suppress unused signal warnings.

uio_out and uio_oe are statically assigned to zero.

## How to Test

To verify the `tt_um_ppm` module, a testbench (`test.py`) written in **Cocotb** is used.  
It sets up a clock, resets the module, provides values to `ui_in`, and checks whether the pulse appears at the correct time in `uo_out[7]`.

---

### Example Test Scenarios

| Time (clock cycles) | `ui_in` (Pulse Position) | Expected Behavior           |
|----------------------|---------------------------|-----------------------------|
| 0 – 10               | 0                         | Pulse at cycle 0            |
| 10 – 266             | 20                        | Pulse at cycle 20           |
| 266 – 522            | 100                       | Pulse at cycle 100          |
| 522 – 778            | 255                       | Pulse at cycle 255          |
| 778 – 1034           | 5                         | Pulse at cycle 5            |

---

### Observations

- The **pulse is always one clock cycle wide**.
- The output `uo_out[7]` is **asserted HIGH only when the internal counter equals `ui_in`**.
- The remaining bits of `uo_out` **remain LOW** at all times.

---

### Monitoring Output (Verilog)

To trace the behavior during simulation, insert the following `$monitor` statement inside a Verilog testbench:

```verilog
initial begin
    $monitor("Time=%0t | ui_in=%d counter=%d | pulse_out=%b",
              $time, ui_in, counter, uo_out[7]);
end
