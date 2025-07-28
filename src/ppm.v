/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_ppm (
    input  wire [7:0] ui_in,    // 8-bit input: Pulse position (0 to 255)
    output wire [7:0] uo_out,   // Output: 1-bit pulse indicator (pulse on MSB bit)
    input  wire [7:0] uio_in,   // Not used
    output wire [7:0] uio_out,  // Not used
    output wire [7:0] uio_oe,   // Not used
    input  wire       ena,      // Always 1
    input  wire       clk,      // Clock input
    input  wire       rst_n     // Active-low reset
);

    reg [7:0] counter;
    reg       pulse;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            counter <= 8'd0;
            pulse   <= 1'b0;
        end else begin
            // Generate pulse at the ui_in position
            if (counter == ui_in) begin
                pulse <= 1'b1;
            end else begin
                pulse <= 1'b0;
            end

            // Increment counter (wrap at 255)
            counter <= counter + 1;
        end
    end

    // Assign pulse to MSB of output, others are zero
    assign uo_out  = {pulse, 7'b0};
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // Prevent unused input warnings
    wire _unused = &{ena,clk ,uio_in, rst_n, 1'b0};

endmodule
