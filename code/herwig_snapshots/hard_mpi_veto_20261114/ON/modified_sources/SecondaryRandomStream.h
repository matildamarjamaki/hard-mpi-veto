#ifndef HERWIG_SECONDARY_RANDOM_STREAM_H
#define HERWIG_SECONDARY_RANDOM_STREAM_H

#include <ThePEG/Repository/UseRandom.h>
#include <ThePEG/Repository/StandardRandom.h>

namespace HerwigRNG {

inline ThePEG::RanGenPtr secondaryRandomStream() {
  static ThePEG::RanGenPtr rng =
      ThePEG::new_ptr(ThePEG::StandardRandom());

  static bool initialized = false;

  if (!initialized) {
    rng->setSeed(987654322L);
    initialized = true;
  }

  return rng;
}

}

#endif
