'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { briefsApi, type EventBrief } from '@/lib/api/briefs'
import { Button } from '@/components/ui/button'
import {
  Calendar,
  Users,
  MapPin,
  DollarSign,
  Utensils,
  Wine,
  Mic,
  Accessibility,
  MessageSquare,
  ArrowLeft,
  Trash2,
} from 'lucide-react'

export default function BriefDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [brief, setBrief] = useState<EventBrief | null>(null)
  const [loading, setLoading] = useState(true)
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    const loadBrief = async () => {
      try {
        const id = parseInt(params.id as string)
        const data = await briefsApi.get(id)
        setBrief(data)
      } catch (err) {
        console.error('Failed to load brief:', err)
      } finally {
        setLoading(false)
      }
    }

    loadBrief()
  }, [params.id])

  const handleDelete = async () => {
    if (!brief) return

    if (
      !confirm(
        'Are you sure you want to delete this brief? This action cannot be undone.'
      )
    ) {
      return
    }

    setDeleting(true)
    try {
      await briefsApi.delete(brief.id)
      router.push('/host/dashboard')
    } catch (err) {
      alert('Failed to delete brief')
      setDeleting(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  if (!brief) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground mb-4">Brief not found</p>
          <Button onClick={() => router.push('/host/dashboard')}>
            Back to Dashboard
          </Button>
        </div>
      </div>
    )
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
  }

  const formatEventType = (type: string) => {
    return type
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  const formatBorough = (borough: string | null) => {
    if (!borough) return 'Any borough'
    return borough
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  const formatEnum = (value: string) => {
    return value
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400'
      case 'matched':
        return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      case 'booked':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-400'
      case 'completed':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Back button */}
        <Button
          variant="ghost"
          onClick={() => router.push('/host/dashboard')}
          className="mb-6"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Dashboard
        </Button>

        {/* Header */}
        <div className="bg-card border rounded-lg p-6 mb-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold mb-2">
                {formatEventType(brief.event_type)}
              </h1>
              <p className="text-muted-foreground">
                Created on {formatDate(brief.created_at)}
              </p>
            </div>
            <span
              className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
                brief.status
              )}`}
            >
              {brief.status.charAt(0).toUpperCase() + brief.status.slice(1)}
            </span>
          </div>
        </div>

        {/* Details grid */}
        <div className="grid gap-6 md:grid-cols-2 mb-6">
          {/* Basic Info */}
          <div className="bg-card border rounded-lg p-6">
            <h2 className="text-lg font-semibold mb-4">Event Details</h2>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <Calendar className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <p className="font-medium">Date</p>
                  <p className="text-sm text-muted-foreground">
                    {formatDate(brief.date_preferred)}
                  </p>
                  {brief.date_flexible && (
                    <p className="text-xs text-muted-foreground mt-1">
                      Flexible (±1 week)
                    </p>
                  )}
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Users className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <p className="font-medium">Guests</p>
                  <p className="text-sm text-muted-foreground">
                    {brief.headcount} people
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <MapPin className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <p className="font-medium">Location</p>
                  <p className="text-sm text-muted-foreground">
                    {formatBorough(brief.borough_pref)}
                  </p>
                  {brief.neighborhood_pref && (
                    <p className="text-xs text-muted-foreground mt-1">
                      {brief.neighborhood_pref}
                    </p>
                  )}
                </div>
              </div>

              <div className="flex items-start gap-3">
                <DollarSign className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <p className="font-medium">Budget</p>
                  <p className="text-sm text-muted-foreground">
                    {brief.budget_min ? `$${brief.budget_min} - ` : 'Up to '}$
                    {brief.budget_max}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Requirements */}
          <div className="bg-card border rounded-lg p-6">
            <h2 className="text-lg font-semibold mb-4">Requirements</h2>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <Utensils className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <p className="font-medium">Food & Beverage</p>
                  <p className="text-sm text-muted-foreground">
                    {formatEnum(brief.food_bev_level)}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Wine className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <p className="font-medium">Alcohol</p>
                  <p className="text-sm text-muted-foreground">
                    {formatEnum(brief.alcohol_level)}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Mic className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <p className="font-medium">AV Equipment</p>
                  <p className="text-sm text-muted-foreground">
                    {formatEnum(brief.av_needs)}
                  </p>
                </div>
              </div>

              {brief.accessibility_needs && (
                <div className="flex items-start gap-3">
                  <Accessibility className="w-5 h-5 text-muted-foreground mt-0.5" />
                  <div>
                    <p className="font-medium">Accessibility</p>
                    <p className="text-sm text-muted-foreground">
                      {brief.accessibility_needs}
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Additional Info */}
        {(brief.vibe || brief.notes) && (
          <div className="bg-card border rounded-lg p-6 mb-6">
            <h2 className="text-lg font-semibold mb-4">Additional Details</h2>
            <div className="space-y-4">
              {brief.vibe && (
                <div>
                  <p className="font-medium mb-1">Event Vibe</p>
                  <p className="text-sm text-muted-foreground">{brief.vibe}</p>
                </div>
              )}
              {brief.notes && (
                <div className="flex items-start gap-3">
                  <MessageSquare className="w-5 h-5 text-muted-foreground mt-0.5" />
                  <div>
                    <p className="font-medium mb-1">Notes</p>
                    <p className="text-sm text-muted-foreground">{brief.notes}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          <Button
            variant="destructive"
            onClick={handleDelete}
            disabled={deleting}
            className="ml-auto"
          >
            <Trash2 className="w-4 h-4 mr-2" />
            {deleting ? 'Deleting...' : 'Delete Brief'}
          </Button>
        </div>
      </div>
    </div>
  )
}
