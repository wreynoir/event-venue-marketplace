'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { briefsApi, type EventBriefCreate } from '@/lib/api/briefs'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { ChevronLeft, ChevronRight } from 'lucide-react'

const TOTAL_STEPS = 8

const EVENT_TYPES = [
  { value: 'corporate', label: 'Corporate Event' },
  { value: 'wedding', label: 'Wedding' },
  { value: 'birthday', label: 'Birthday Party' },
  { value: 'anniversary', label: 'Anniversary' },
  { value: 'networking', label: 'Networking Event' },
  { value: 'conference', label: 'Conference' },
  { value: 'other', label: 'Other' },
]

const BOROUGHS = [
  { value: 'manhattan', label: 'Manhattan' },
  { value: 'brooklyn', label: 'Brooklyn' },
  { value: 'queens', label: 'Queens' },
  { value: 'bronx', label: 'Bronx' },
  { value: 'staten_island', label: 'Staten Island' },
]

const FOOD_BEV_LEVELS = [
  { value: 'none', label: 'Not Needed' },
  { value: 'light_bites', label: 'Light Bites' },
  { value: 'full_catering', label: 'Full Catering' },
]

const ALCOHOL_LEVELS = [
  { value: 'none', label: 'No Alcohol' },
  { value: 'beer_wine', label: 'Beer & Wine' },
  { value: 'full_bar', label: 'Full Bar' },
]

const AV_NEEDS = [
  { value: 'none', label: 'Not Needed' },
  { value: 'basic_mic', label: 'Basic Microphone' },
  { value: 'full_setup', label: 'Full AV Setup' },
]

export default function NewBriefPage() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(1)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [formData, setFormData] = useState<Partial<EventBriefCreate>>({
    event_type: 'corporate',
    headcount: 50,
    date_flexible: false,
    food_bev_level: 'none',
    alcohol_level: 'none',
    av_needs: 'none',
  })

  const updateFormData = (field: string, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const nextStep = () => {
    if (currentStep < TOTAL_STEPS) {
      setCurrentStep((prev) => prev + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep((prev) => prev - 1)
    }
  }

  const handleSubmit = async () => {
    setIsSubmitting(true)
    setError(null)

    try {
      // Validate required fields
      if (
        !formData.event_type ||
        !formData.headcount ||
        !formData.date_preferred ||
        !formData.budget_max
      ) {
        setError('Please fill in all required fields')
        setIsSubmitting(false)
        return
      }

      const brief = await briefsApi.create(formData as EventBriefCreate)
      router.push(`/brief/${brief.id}/confirmation`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create brief')
      setIsSubmitting(false)
    }
  }

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-4">
            <div>
              <h2 className="text-2xl font-bold mb-2">What type of event?</h2>
              <p className="text-muted-foreground mb-4">
                Help us find the perfect venue for your occasion
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="event_type">Event Type</Label>
              <Select
                value={formData.event_type}
                onValueChange={(value) => updateFormData('event_type', value)}
              >
                <SelectTrigger id="event_type">
                  <SelectValue placeholder="Select event type" />
                </SelectTrigger>
                <SelectContent>
                  {EVENT_TYPES.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        )

      case 2:
        return (
          <div className="space-y-4">
            <div>
              <h2 className="text-2xl font-bold mb-2">How many guests?</h2>
              <p className="text-muted-foreground mb-4">
                Approximate headcount is fine
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="headcount">Number of Guests</Label>
              <Input
                id="headcount"
                type="number"
                min="1"
                value={formData.headcount || ''}
                onChange={(e) =>
                  updateFormData('headcount', parseInt(e.target.value) || 0)
                }
                placeholder="50"
              />
            </div>
          </div>
        )

      case 3:
        return (
          <div className="space-y-4">
            <div>
              <h2 className="text-2xl font-bold mb-2">When is your event?</h2>
              <p className="text-muted-foreground mb-4">Preferred date</p>
            </div>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="date_preferred">Event Date</Label>
                <Input
                  id="date_preferred"
                  type="date"
                  value={formData.date_preferred || ''}
                  onChange={(e) =>
                    updateFormData('date_preferred', e.target.value)
                  }
                />
              </div>
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="date_flexible"
                  checked={formData.date_flexible}
                  onChange={(e) =>
                    updateFormData('date_flexible', e.target.checked)
                  }
                  className="h-4 w-4 rounded border-gray-300"
                />
                <Label htmlFor="date_flexible" className="font-normal">
                  I'm flexible with the date (±1 week)
                </Label>
              </div>
            </div>
          </div>
        )

      case 4:
        return (
          <div className="space-y-4">
            <div>
              <h2 className="text-2xl font-bold mb-2">Where in NYC?</h2>
              <p className="text-muted-foreground mb-4">
                Location preferences (optional)
              </p>
            </div>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="borough_pref">Preferred Borough (Optional)</Label>
                <Select
                  value={formData.borough_pref || undefined}
                  onValueChange={(value) =>
                    updateFormData('borough_pref', value || null)
                  }
                >
                  <SelectTrigger id="borough_pref">
                    <SelectValue placeholder="Any borough" />
                  </SelectTrigger>
                  <SelectContent>
                    {BOROUGHS.map((borough) => (
                      <SelectItem key={borough.value} value={borough.value}>
                        {borough.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="neighborhood_pref">
                  Neighborhood (Optional)
                </Label>
                <Input
                  id="neighborhood_pref"
                  value={formData.neighborhood_pref || ''}
                  onChange={(e) =>
                    updateFormData('neighborhood_pref', e.target.value || null)
                  }
                  placeholder="e.g., SoHo, Williamsburg"
                />
              </div>
            </div>
          </div>
        )

      case 5:
        return (
          <div className="space-y-4">
            <div>
              <h2 className="text-2xl font-bold mb-2">What's your budget?</h2>
              <p className="text-muted-foreground mb-4">
                Helps us match you with the right venues
              </p>
            </div>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="budget_max">Maximum Budget ($)</Label>
                <Input
                  id="budget_max"
                  type="number"
                  min="0"
                  step="100"
                  value={formData.budget_max || ''}
                  onChange={(e) =>
                    updateFormData('budget_max', parseFloat(e.target.value) || 0)
                  }
                  placeholder="5000"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="budget_min">Minimum Budget (Optional)</Label>
                <Input
                  id="budget_min"
                  type="number"
                  min="0"
                  step="100"
                  value={formData.budget_min || ''}
                  onChange={(e) =>
                    updateFormData(
                      'budget_min',
                      e.target.value ? parseFloat(e.target.value) : null
                    )
                  }
                  placeholder="2000"
                />
              </div>
            </div>
          </div>
        )

      case 6:
        return (
          <div className="space-y-4">
            <div>
              <h2 className="text-2xl font-bold mb-2">Food & Beverage?</h2>
              <p className="text-muted-foreground mb-4">
                What level of catering do you need?
              </p>
            </div>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="food_bev_level">Food Service</Label>
                <Select
                  value={formData.food_bev_level}
                  onValueChange={(value) =>
                    updateFormData('food_bev_level', value)
                  }
                >
                  <SelectTrigger id="food_bev_level">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {FOOD_BEV_LEVELS.map((level) => (
                      <SelectItem key={level.value} value={level.value}>
                        {level.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="alcohol_level">Alcohol Service</Label>
                <Select
                  value={formData.alcohol_level}
                  onValueChange={(value) =>
                    updateFormData('alcohol_level', value)
                  }
                >
                  <SelectTrigger id="alcohol_level">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {ALCOHOL_LEVELS.map((level) => (
                      <SelectItem key={level.value} value={level.value}>
                        {level.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        )

      case 7:
        return (
          <div className="space-y-4">
            <div>
              <h2 className="text-2xl font-bold mb-2">
                Audio/Visual & Accessibility
              </h2>
              <p className="text-muted-foreground mb-4">
                Any special requirements?
              </p>
            </div>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="av_needs">AV Equipment Needs</Label>
                <Select
                  value={formData.av_needs}
                  onValueChange={(value) => updateFormData('av_needs', value)}
                >
                  <SelectTrigger id="av_needs">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {AV_NEEDS.map((need) => (
                      <SelectItem key={need.value} value={need.value}>
                        {need.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="accessibility_needs">
                  Accessibility Needs (Optional)
                </Label>
                <Textarea
                  id="accessibility_needs"
                  value={formData.accessibility_needs || ''}
                  onChange={(e) =>
                    updateFormData(
                      'accessibility_needs',
                      e.target.value || null
                    )
                  }
                  placeholder="Wheelchair accessible, elevator required, etc."
                  rows={3}
                />
              </div>
            </div>
          </div>
        )

      case 8:
        return (
          <div className="space-y-4">
            <div>
              <h2 className="text-2xl font-bold mb-2">Final touches</h2>
              <p className="text-muted-foreground mb-4">
                Tell us about the vibe and any other details
              </p>
            </div>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="vibe">Event Vibe (Optional)</Label>
                <Input
                  id="vibe"
                  value={formData.vibe || ''}
                  onChange={(e) =>
                    updateFormData('vibe', e.target.value || null)
                  }
                  placeholder="e.g., casual, formal, creative"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="notes">Additional Notes (Optional)</Label>
                <Textarea
                  id="notes"
                  value={formData.notes || ''}
                  onChange={(e) =>
                    updateFormData('notes', e.target.value || null)
                  }
                  placeholder="Any other details we should know..."
                  rows={4}
                />
              </div>
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header with progress */}
      <div className="sticky top-0 bg-background border-b z-10">
        <div className="max-w-2xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between mb-2">
            <h1 className="text-lg font-semibold">Create Event Brief</h1>
            <span className="text-sm text-muted-foreground">
              {currentStep} / {TOTAL_STEPS}
            </span>
          </div>
          {/* Progress bar */}
          <div className="w-full bg-secondary rounded-full h-2">
            <div
              className="bg-primary h-2 rounded-full transition-all duration-300"
              style={{ width: `${(currentStep / TOTAL_STEPS) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="max-w-2xl mx-auto px-4 py-8">
        {error && (
          <div className="mb-4 p-4 bg-destructive/10 border border-destructive rounded-lg text-destructive">
            {error}
          </div>
        )}

        <div className="mb-8">{renderStep()}</div>

        {/* Navigation buttons */}
        <div className="flex gap-3">
          {currentStep > 1 && (
            <Button
              variant="outline"
              onClick={prevStep}
              className="flex-1"
              disabled={isSubmitting}
            >
              <ChevronLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
          )}

          {currentStep < TOTAL_STEPS ? (
            <Button onClick={nextStep} className="flex-1">
              Next
              <ChevronRight className="w-4 h-4 ml-2" />
            </Button>
          ) : (
            <Button
              onClick={handleSubmit}
              className="flex-1"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Submitting...' : 'Submit Brief'}
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
