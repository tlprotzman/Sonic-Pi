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
  #stop
  sample :bd_haus, rate: 0.9, amp: 2
  sleep 1
end

live_loop :drums_two do
  #stop
  sleep 1
  sample :drum_snare_soft, rate: 1.5, amp: 1.5
  sleep 1
end# Welcome to Sonic Pi v2.10

