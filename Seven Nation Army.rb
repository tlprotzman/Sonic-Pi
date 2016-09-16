use_bpm 130

live_loop :riff_one do
  with_fx :distortion  do
    use_synth :subpulse
    play :a2, release: 1.5
    sleep 1.5
    play :a2, sustain: 0.5, release: 0.1
    sleep 0.5
    play :c3, attack_level: 0.2, sustain: 0.5, release: 0.1
    sleep 0.6666
    play :a2, sustain: 0.5, release: 0.1
    sleep 0.6666
    play :g2, sustain: 0.5, release: 0.1
    sleep 0.6666
    play :f2, sustain: 1, release: 1
    sleep 2
    play :e2, sustain: 1, release: 1
    sleep 2
  end
end

live_loop :drums_one do
  sample :bd_haus, rate: 0.8, amp: 2
  sleep 1
end